"""
Module to create neural network
"""
import random
import math
import numpy
import copy
e = 2.718

def sigmoid(x):
    """
    Returns the sigmoid of x
    :rtype: number
    """
    return (math.pow(e, x)) / ((math.pow(e, x)) + 1)

class Neuron:
    """
    An indvidual node in a network
    """
    def __init__(self):
        """
        Initialize a neuron
        """
        self.bias = 0#random.random() #Neuron bias value
        self.value = 0
        
    def activate(self):
        """
        Activates the neuron by computing the sigmoid of its value
        """
        self.value = sigmoid(self.value)
        
    def setValue(self, value):
        """
        Directly set the value inside the neuron
        """
        self.value = value

class Synapse:
    """
    A synapse is a connection between two neurons with a weight.
    """
    def __init__(self, leftNeuron, rightNeuron):
        """
        Initalize the synapse given the neuron on the left side and the right side
        """
        self.leftNeuron = leftNeuron
        self.rightNeuron = rightNeuron
        self.weight = numpy.random.normal(1, 0.1, 1)
        #print(self.weight)
        
    def fire(self):
        """
        Fire the synapse by pulling the value from the left neuron, multiplying by the weight, 
        then adding it to the value of the right neuron.
        """
        self.rightNeuron.value += (self.leftNeuron.value * self.weight) + self.rightNeuron.bias

    def __str__(self):
        """
        Converts a synapse to a string for debuging proposes.
        """
        return ( "l neuron value:", '\t' + str(self.leftNeuron.value) + 
            '\t', "r neuron value:", '\t' + str(self.rightNeuron.value) )
    
    def mutate(self):
        """
        Randomly adjusts the weight of the synapse
        """
        self.weight += random.uniform(-0.1, 0.1)


class NeuralNetwork:
    """
    A layered conglumerate of synapses and neurons
    
    Initialize it given the number of inputs and outputs.
    """
    def __init__(self, numInputs, numOutputs):
        """
        First argument is the number of input nodes
        Second argument is the number of output nodes
        
        There is always one fully hidden connected layer with the same number of nodes as the 
        input layer.
        """
        self.fitness = 0
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
        """
        Set the value of every neuron in the network to zero.
        """
        for neuron in self.hiddenLayer:
            neuron.setValue(0)
        for neuron in self.outputLayer:
            neuron.setValue(0)

    def fireNetwork(self, inputList):
        """
        Fire the network given a list of inputs
        
        The length of the input list must equal the size of the input layer.
        :return: An output list of the same length as the input list.
        """
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
        
    def getSynapses(self):
        """
        Returns a concatenation of all the synapses
        """
        return self.inputLayer + self.hiddenLayer + self.outputLayer
        
    def printSynapses(self):
        """
        Print the synapses
        """
        counter = 0
        for synapse in self.hiddenLayerSynapses:
            print (counter, " ", synapse.__str__())
            counter += 1
        for synapse in self.outputLayerSynapses:
            print (counter, " ", synapse.__str__())
            counter += 1
    def cloneNetwork(self):
        return copy.deepcopy(self)