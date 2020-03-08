import random
import math
import numpy
e = 2.718

def sigmoid(x):
    return (math.pow(e,x)) / ((math.pow(e,x)) + 1)

class Neuron:
    def __init__(self): 
        self.bias = 0#random.random() #Neuron bias value
        self.value = 0
    
    def activate(self):
        self.value = sigmoid(self.value)
    
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
        self.weight = numpy.random.normal(1, 0.1, 1)
        print(self.weight)
    
    def fire(self):
        self.rightNeuron.value += (self.leftNeuron.value * self.weight) + self.rightNeuron.bias

    def __str__(self):
        return "l neuron value:" , '\t' + str(self.leftNeuron.value)+ '\t', "r neuron value:", '\t' + str(self.rightNeuron.value)


class NeuralNetwork:
    def __init__(self, numInputs, numOutputs):
        self.inputLayer = []
        for i in range(numInputs):
            self.inputLayer.append(Neuron())

        self.hiddenLayer = []
        self.hiddenLayerSynapses = []
        for i in range(numInputs):
            neuron = Neuron()
            self.hiddenLayer.append(neuron)
            for j in range(numInputs):
                synapse = Synapse(self.inputLayer[j], neuron)
                self.hiddenLayerSynapses.append(synapse)

        self.outputLayer = []
        self.outputLayerSynapses = []
        for i in range(numOutputs):
            neuron = Neuron()
            self.outputLayer.append(neuron)
            for j in range(len(self.hiddenLayer)):
                synapse = Synapse(self.hiddenLayer[j], neuron)
                self.outputLayerSynapses.append(synapse)
    
    def clearNeurons(self):
        for neuron in self.hiddenLayer:
            neuron.setValue(0)
        for neuron in self.outputLayer:
            neuron.setValue(0)

    def fireNetwork(self, inputList):
        if len(inputList) != len(self.inputLayer):
            raise ValueError("Number of inputs did not match number of inputs on neural network.")
        
        self.clearNeurons()
        for i in range(len(inputList)):
            self.inputLayer[i].setValue(inputList[i])

        for synapse in self.hiddenLayerSynapses:
            synapse.fire()

        for neuron in self.hiddenLayer:
            neuron.activate()

        for synapse in self.outputLayerSynapses:
            synapse.fire()

        for neuron in self.outputLayer:
            neuron.activate()
        output = []
        for neuron in self.outputLayer:
            output.append(neuron.value)
        #self.clearNeurons()
        return output

    def printSynapses(self):
        counter = 0
        for synapse in self.hiddenLayerSynapses:
            print (counter, " ", synapse.__str__())
            counter += 1
        for synapse in self.outputLayerSynapses:
            print (counter, " ", synapse.__str__())
            counter += 1
