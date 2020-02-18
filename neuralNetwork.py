import random
import math
e = 2.718

def sigmoid(x):
    return (math.pow(e,x)) / ((math.pow(e,x)) + 1)

class Neuron:
    def __init__(self): 
        self.bias = 0 #random.random() #Neuron bias value
        self.value = 0
    
    def calculate(self):
        return sigmoid(value)
    
    def popValue(self):
        x = self.value
        self.value = 0
        return x
    
    def setValue(self, value):
        self.value = value

class Synapse:
    def __init__(self, leftNeuron, rightNeuron):
        self.leftNeuron = leftNeuron
        self.rightNeuron = rightNeuron
        self.weight = random.random()
    
    def fire(self):
        self.rightNeuron.value += (self.leftNeuron.value * self.weight) #+ self.rightNeuron.bias

