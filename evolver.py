"""
Module to evolve the Neural Networks
"""
import neuralNetwork as nn
import nintaco
import math
import random

class Evolver:
    """
    Class that handles mutations, keeping track of the fitness,
    and creating new populations.
    """
    def __init__(self, api, populationSize = 6, mutationRate = 0.1):
        """
        initalizes an evolver
        """
        self.populationSize = populationSize
        self.api = api
        self.mutationRate = mutationRate
        self.spamStart = False
        self.spamDirection = False
        self.generationCount = 0
        self.population = []
        for i in range(self.populationSize):
            self.population.append(nn.NeuralNetwork(10, 4))
        self.currentNetwork = self.population[0]
        self.currentNetworkIndex = 0
        self.lastLifeCount = 3
    
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
    
    def generateNewPopulation(self):
        """
        Generates a new population based off most fit network
        """
        self.generationCount += 1
        print("Generating a new population: Generation # ", self.generationCount)
        mostFitNetwork = self.population[0]
        newPopulation = []
        #Finds the most fit network
        for network in self.population:
            if network.fitness > mostFitNetwork.fitness:
                mostFitNetwork = network
        #Generates 9 new mutants from the most fit network     
        print("The most fit network in this generation had a fitness of: ", mostFitNetwork.fitness)
        print("It's synapses were:")
        mostFitNetwork.printSynapses()
        for i in range(self.populationSize - 1):
            newNetwork = mostFitNetwork.clone()
            self.mutateNetwork(newNetwork)
            newPopulation.append(newNetwork)
        #Orignal most fit network    
        newPopulation.append(mostFitNetwork)
        self.population = newPopulation
        self.currentNetworkIndex = 0
        self.currentNetwork = self.population[0]
        for network in self.population:
            network.fitness = 0 #Set fitness to zero on every new network.
    
    def playGame(self):
        """
        Plays the game with the current network.
        This function is called every emulator frame.
        """
        if self.spamStart:
            api.writeGamepad(0, 3, self.spamDirection) #Start button
            self.spamDirection = not self.spamDirection
        
        #Pacman's X and Y coordinates based on his memory address
        pacmanX = api.peekCPU(0x001A) / 255.0
        pacmanY = api.peekCPU(0x001C) / 255.0
        
        #Pinky's X and Y coordinates based on his memory address.
        pinkyX = api.peekCPU(0x0022) / 255.0
        pinkyY = api.peekCPU(0x0024) / 255.0
        
        blinkyX = api.peekCPU(0x001E) / 255.0
        blinkyY = api.peekCPU(0x0020) / 255.0
        
        inkyX = api.peekCPU(0x0026) / 255.0
        inkyY = api.peekCPU(0x0028) / 255.0
        
        clydeX = api.peekCPU(0x002A) / 255.0
        clydeY = api.peekCPU(0x002C) / 255.0
        
        output = self.currentNetwork.fireNetwork([pacmanX, pacmanY,
        pinkyX, pinkyY,
        blinkyX, blinkyY,
        inkyX, inkyY,
        clydeX, clydeY
        ])
        m = max(output)
        if output[0] >= m:
            api.writeGamepad(0, 4, True) # Gamepad 0, 4 = up, True = pressed
        elif output[1] >= m:
            api.writeGamepad(0, 5, True) # down
        elif output[2] >= m:
            api.writeGamepad(0, 6, True) # left
        elif output[3] >= m:
            api.writeGamepad(0, 7, True) # right
        self.currentNetwork.fitness = self.getCurrentFitness()
    
    def incrementNetwork(self):
        """
        Increments the current network to the next one.
        """
        print("Incrementing network, score was ", self.currentNetwork.fitness)
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

nintaco.initRemoteAPI("localhost", 9999)
api = nintaco.getAPI()
evolver = Evolver(api)
api.addFrameListener(evolver.playGame)
api.addAccessPointListener(evolver.onLifeCountChanged, nintaco.PostWrite, 0x0067)
api.run()