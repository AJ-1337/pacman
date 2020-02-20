import sys
import nintaco
import math
import neuralNetwork

nintaco.initRemoteAPI("localhost", 9999)
api = nintaco.getAPI()

def init():
    #api.open("Pacman.nes")
    api.setSpeed(-1)
    api.loadState("startState.save")

neuralNetworks = []
for i in range(10):
    nn = neuralNetwork.NeuralNetwork(10, 4)
    neuralNetworks.append(nn)

def test():
    pacmanX = api.peekCPU(0x001A) / 255.0
    pacmanY = api.peekCPU(0x001C) / 255.0
    
    blinkyX = api.peekCPU(0x001E) / 255.0
    blinkyY = api.peekCPU(0x0020) / 255.0
    
    pinkyX = api.peekCPU(0x0022) / 255.0
    pinkyY = api.peekCPU(0x0024) / 255.0
    
    inkyX = api.peekCPU(0x0026) / 255.0
    inkyY = api.peekCPU(0x0028) / 255.0
    
    clydeX = api.peekCPU(0x002A) / 255.0
    clydeY = api.peekCPU(0x002C) / 255.0
    
    alive = api.peekCPU(0x00DB) == 0
    if not alive:
        init()

api.addFrameListener(test)
api.run()