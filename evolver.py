"""
Module to evolve the Neural Networks
"""
import neuralNetwork as nn
import math
import random
import time

class Evolver:
    """
    Class that handles mutations, keeping track of the fitness,
    and creating new populations.
    """
    def __init__(self, api, populationSize = 20, mutationRate = 0.1, maxGenerations = 0, showResults = True):
        """
        initalizes an evolver
        """
        self.populationSize = populationSize
        self.api = api
        self.originalMutationRate = mutationRate
        self.mutationRate = mutationRate
        self.spamStart = False
        self.spamDirection = False
        self.generationCount = 1
        self.maxGenerations = maxGenerations
        self.population = []
        for i in range(self.populationSize):
            self.population.append(nn.NeuralNetwork(10, 4))
        self.currentNetwork = self.population[0]
        self.currentNetworkIndex = 0
        self.lastLifeCount = 3
        self.initialFitness = 0
        self.bestFitness = 0
        self.startTime = time.time()
        self.showResults = showResults
    
    def getCurrentFitness(self):
        """
        Gets the fitness of current running network (score of the game)
        """
        fitness = 0
        digit = 1
        #Goes through each digit in the current score and adds them.
        for address in range(0x0070, 0x0075 + 1):
            fitness = fitness + ((self.api.peekCPU(address)) * digit)
            digit *= 10
        return fitness * 10
    def mutateNetwork(self, network):
        """
        Mutates the weights of the synapses in the network
        """
        synapseList = network.getSynapses()
        for synapse in synapseList:
            #If roll is less than mutation rate, this mutates the synapse.
            roll = random.uniform(0, 1)
            if roll < self.mutationRate:
                synapse.mutate()
    
    def printResultsReport(self):
        print("The AI began with a fitness of ", self.initialFitness)
        print("It ran for a total of ", self.generationCount, " generations.")
        print("It's best fitness was ", self.bestFitness)
        print("This represents an average improvement of ", float(self.bestFitness - self.initialFitness) / (self.generationCount - 1), " points per generation.")
        print("The evolver ran for a total of ", time.time() - self.startTime, " seconds")
    
    def generateNewPopulation(self, keepBestProportion = 0.1, keepRandomProportion = 0.1):
        """
        Generates a new population based off most fit network
        keepBestProportion refers to the proportion of the most fit members
        of the population that should be kept. keepRandomProportion refers
        to the proportion of other random members of the population that
        should be kept. Numbers are rounded down when not whole.
        
        """

        mostFitNetwork = self.population[0]
        networksToKeep = []
        newPopulation = []
        
        #Sort the network from most fit to least fit
        self.population.sort(key = lambda x: x.fitness, reverse = True)
        numBestToKeep = int(keepBestProportion * self.populationSize)
        numRandomToKeep = int(keepRandomProportion * self.populationSize)
        numToKeep = numBestToKeep + numRandomToKeep
        numOffspringPerNetwork = int( (self.populationSize / numToKeep) - 1 )
        
        networksToKeep.extend(self.population[0:numBestToKeep]) #Immediately append the "keepers"
        randomKeepers = random.sample(self.population[numBestToKeep:], numRandomToKeep)
        networksToKeep.extend(randomKeepers)
        mostFitNetwork = self.population[0]
        #Generates 9 new mutants from the most fit network     
        print("The most fit network in this generation had a fitness of: ", mostFitNetwork.fitness)
        
        if self.generationCount == 1:
            self.initialFitness = mostFitNetwork.fitness
            self.bestFitness = mostFitNetwork.fitness
        else:
            self.bestFitness = max(self.bestFitness, mostFitNetwork.fitness)
            
        if self.maxGenerations!=0 and self.generationCount >= self.maxGenerations:
            self.api.removeFrameListener(self.playGame)
            self.api.setPaused(True)
            if self.showResults:
                self.printResultsReport()
                return
        print("Generating a new population: Generation # ", self.generationCount)
        
        #Generate the offspring from the networks we've selected to keep.
        for network in networksToKeep:
            newPopulation.append(network) #Put the parent in, it survived
            for i in range(numOffspringPerNetwork): #Produce it's children
                offspring = network.clone()
                self.mutateNetwork(offspring)
                newPopulation.append(offspring) 
        self.population = newPopulation
        self.currentNetworkIndex = 0
        self.currentNetwork = self.population[0]
        for network in self.population:
            network.fitness = 0 #Set fitness to zero on every new network.
        self.generationCount += 1
    
    def playGame(self):
        """
        Plays the game with the current network.
        This function is called every emulator frame.
        """
        if self.spamStart:
            self.api.writeGamepad(0, 3, self.spamDirection) #Start button
            self.spamDirection = not self.spamDirection
        
        #Pacman's X and Y coordinates based on his memory address
        pacmanX = self.api.peekCPU(0x001A) / 255.0
        pacmanY = self.api.peekCPU(0x001C) / 255.0
        
        #Pinky's X and Y coordinates based on his memory address.
        pinkyX = self.api.peekCPU(0x0022) / 255.0
        pinkyY = self.api.peekCPU(0x0024) / 255.0
        
        blinkyX = self.api.peekCPU(0x001E) / 255.0
        blinkyY = self.api.peekCPU(0x0020) / 255.0
        
        inkyX = self.api.peekCPU(0x0026) / 255.0
        inkyY = self.api.peekCPU(0x0028) / 255.0
        
        clydeX = self.api.peekCPU(0x002A) / 255.0
        clydeY = self.api.peekCPU(0x002C) / 255.0
        
        output = self.currentNetwork.fireNetwork([pacmanX, pacmanY,
        pinkyX, pinkyY,
        blinkyX, blinkyY,
        inkyX, inkyY,
        clydeX, clydeY
        ])
        m = max(output)
        if output[0] >= m:
            self.api.writeGamepad(0, 4, True) # Gamepad 0, 4 = up, True = pressed
        elif output[1] >= m:
            self.api.writeGamepad(0, 5, True) # down
        elif output[2] >= m:
            self.api.writeGamepad(0, 6, True) # left
        elif output[3] >= m:
            self.api.writeGamepad(0, 7, True) # right
        self.currentNetwork.fitness = self.getCurrentFitness()
    
    def incrementNetwork(self):
        """
        Increments the current network to the next one.
        """
        print("Network #", self.currentNetworkIndex, ", Incrementing network, score was ", self.currentNetwork.fitness)
        self.spamStart = True
        if self.currentNetworkIndex >= self.populationSize - 1:
            raise ValueError("You cannot increment any further - you're on the last network in the population!")
        self.currentNetworkIndex += 1
        self.currentNetwork = self.population[self.currentNetworkIndex]
    
    def onLifeCountChanged(self, accessPoint, address, value):
        """
        This function is called when
        Pac-Man's life count changes.
        For whatever reason, the emulator
        API actually calls it twice per change:
        the first time with the old value,
        then the second time with the new value.
        (Horrible.)
        """
        if self.lastLifeCount == 1 and value==0: #Out of lives.
            if self.currentNetworkIndex >= self.populationSize - 1: #The last member of this generation died.
                print("Last member of population has died.")
                self.generateNewPopulation()
                self.spamStart = True
            else: #The member died but wasn't the last member of the population.
                self.incrementNetwork()
        if self.lastLifeCount == 0 and value==3:
            self.spamStart = False
        self.lastLifeCount = value
        return -1 #Return no change to value for the emulator API.