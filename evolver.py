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
    def __init__(self, api, populationSize = 10, mutationRate = 0.1):
        """
        initalizes an evolver
        """
        self.populationSize = populationSize
        self.api = api
        self.mutationRate = mutationRate
        self.population = []
        for i in range(self.populationSize):
            self.population.append(nn.NeuralNetwork(10, 4))
    def getFitness(self):
        """
        Gets the fitness of the neural network
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
        mostFitNetwork = self.population[0]
        newPopulation = []
        #Finds the most fit network
        for network in self.population:
            if network.fitness > mostFitNetwork.fitness:
                mostFitNetwork = network
        #Generates 9 new mutants from the most fit network        
        for i in range(self.populationSize - 1):
            newNetwork = mostFitNetwork.clone()
            mutateNetwork(newNetwork)
            newPopulation.append(newNetwork)
        #Orignal most fit network    
        newPopulation.append(mostFitNetwork)
        self.population = newPopulation
            