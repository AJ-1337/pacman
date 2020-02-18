import random
import math
e = 2.718

def sigmoid(x):
    return (math.pow(e,x)) / ((math.pow(e,x)) + 1)

class Neuron:
    def __init__(self): 
        self.synapses = {} #Holds references to other neurons to the left, plus weights
        self.bias = 1 #random.random() #Neuron bias value
        self.value = 0
    
    def calculate(self):
        self.value = 0
        for neuron, weight in self.synapses.items():
            self.value += weight * neuron.value
        self.value = sigmoid(value)
    
    def getValue(self):
        return self.value
    
    def setValue(self, value):
        self.value = value

class NeuralNetwork:
    def __init__(self, numInputs, numHiddenLayers, numOutputs):
        self.layers = {}
        for i in range(2 + numHiddenLayers):
            self.layers[i] = {}
        
        for i in range(numInputs): #Creates all the input neurons.
            self.layers[0][i] = Neuron()
        
        for layer in range(numHiddenLayers):
            for i in range(numInputs):
                neuron = Neuron()
                self.layers[layer + 1][i] = neuron
                for neuron in self.layers[layer - 1]:
                    neuron.synapses[neuron] = random.random()

n = NeuralNetwork(1,1,1)