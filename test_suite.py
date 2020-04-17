import pytest
import neuralNetwork as nn
import evolver as Evolver
import nintaco

nintaco.initRemoteAPI("localhost", 9999)
api = nintaco.getAPI()

#Testing requirements
def test_sendControllerInput(): #Req 1
    evolver = Evolver.Evolver(api)
    def writeAndRead():
        evolver.writeGamepad(Evolver.GAMEPAD_START, True)
        assert api.readGamepad(0, Evolver.GAMEPAD_START)
        evolver.writeGamepad(Evolver.GAMEPAD_START, False)
        assert not api.readGamepad(0, Evolver.GAMEPAD_START)
        api.removeActivateListener(writeAndRead)
        api.stop()
    
    api.addActivateListener(writeAndRead)
    api.run()
    
def test_geneticAlgorithmParameters(): #Req 2
    evolver = Evolver.Evolver(api = api, populationSize = 100, mutationRate = 0.15, maxGenerations = 2, showResults = False)
    assert evolver.populationSize == 100 and evolver.mutationRate==pytest.approx(0.15) and evolver.maxGenerations == 2 and evolver.showResults == False

fitness = -1
def test_getFitness(): #Req 3
    evolver = Evolver.Evolver(api)
    def testFitness():
        global fitness
        fitness = evolver.getCurrentFitness()
        api.removeActivateListener(testFitness)
        api.stop()
    
    api.addActivateListener(testFitness)
    api.run()
    assert fitness >= 0 #Pac-man cannot have a negative score.

def test_cullPoorNetworks(): #Req 4
    evolver = Evolver.Evolver(api, populationSize = 10)
    #We will go through and assign a fake fitness to each network,
    #because we have already determined our fitness checking
    #function works. Then we will have the evolver make a new network
    #and check that the poorest one was in fact removed.
    for network in evolver.population:
        network.fitness = 1000
    evolver.population[0].fitness = 0 #Worst one.
    evolver.population[0]._poorPerformerFlag = True #Set a flag to show that this one is bad.
    evolver.generateNewPopulation(keepBestProportion = 0.1, keepRandomProportion = 0.0)
    for network in evolver.population:
        assert not hasattr(network, "_poorPerformerFlag")
        #Ensures that the poor performer does not exist in the new generation,
        #i.e, it has been culled!

def test_constantOutput(): #Req 5
    evolver = Evolver.Evolver(api)
    assert evolver.printGenerationResults(60)

frameCount = 0
def test_readMemoryByFrame(): #Req 6
    evolver = Evolver.Evolver(api, populationSize = 2, mutationRate = 0.15, maxGenerations = 2, showResults = True, keepBestProportion = 0.5, keepRandomProportion = 0.0)
    def frameCounter():
        global frameCount
        frameCount+=1
        assert frameCount == evolver.frameCount #If the evolver had an error processing the game, the frame counts wont match!
        if frameCount > 25000: #Test 25,000 frames of gameplay, making sure the tester's frame counter never falls out of sync with the evolver.
            api.removeFrameListener(frameCounter)
            api.removeFrameListener(evolver.playGame)
            api.stop()
    api.addFrameListener(frameCounter)
    api.addFrameListener(evolver.playGame)
    api.addAccessPointListener(evolver.onLifeCountChanged, nintaco.PostWrite, 0x0067)
    api.run()

def test_saveNeuralNetwork(): #Req 7
    neuralNetwork = nn.NeuralNetwork(4,4)
    assert neuralNetwork.printSynapses()
#Bonus / supplementary tests for additional coverage
def test_sigmoid():
    assert nn.sigmoid(0) == pytest.approx(0.5)