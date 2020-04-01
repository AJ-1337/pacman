import neuralNetwork as nn
import nintaco
import math
import random

class Evolver:
    def __init__(self, api, populationSize = 10, mutationRate = 0.1):
        self.populationSize = populationSize
        self.api = api
        self.mutationRate = mutationRate
        self.population = []
        for i in range(self.populationSize):
            self.population.append(nn.NeuralNetwork(10, 4))
    def getFitness(self):
        fitness = 0
        digit = 1
        for address in range(0x0070, 0x0075 + 1):
            fitness = fitness + ((self.api.peekCPU(address)) * digit)
            digit *= 10
        return fitness * 10
    def mutateNetwork(self, network):
        synapseList = network.getSynapses()
        for synapse in synapseList:
            roll = random.uniform(0, 1)
            if roll < self.mutationRate:
                synapse.mutate()
    def generateNewPopulation(self):
        mostFitNetwork = self.population[0]
        newPopulation = []
        for network in self.population:
            if network.fitness > mostFitNetwork.fitness:
                mostFitNetwork = network
        for i in range(self.populationSize - 1):
            newNetwork = mostFitNetwork.clone()
            mutateNetwork(newNetwork)
            newPopulation.append(newNetwork)
        newPopulation.append(mostFitNetwork)
        self.population = newPopulation
            