import sys
import nintaco
import math
import neuralNetwork
import evolver

nintaco.initRemoteAPI("localhost", 9999)
api = nintaco.getAPI()
nn = neuralNetwork.NeuralNetwork(10, 4)

lastNearestGhostDistance = 0
evolver1 = evolver.Evolver(api, 10)

def real_test_lol():
    print(evolver1.getFitness())

def test():
    print(evolver1.getFitness())
    #Pacman's X and Y coordinates based on his memory address
    pacmanX = api.peekCPU(0x001A) / 255.0
    pacmanY = api.peekCPU(0x001C) / 255.0
    
    #Pinky's X and Y coordinates based on his memory address.
    pinkyX = api.peekCPU(0x0022) / 255.0
    pinkyY = api.peekCPU(0x0024) / 255.0
    #Calculates the distance from pinky to pacman based on their memory addresses.
    pinkyDistance = math.sqrt( math.pow(pinkyX - pacmanX, 2) + math.pow(pinkyY - pacmanY, 2))

    #Blinky's X and Y coordinates based on his memory address.
    blinkyX = api.peekCPU(0x001E) / 255.0
    blinkyY = api.peekCPU(0x0020) / 255.0
    #Calculates the distance from blinky to pacman based on their memory addresses.
    blinkyDistance = math.sqrt( math.pow(blinkyX - pacmanX, 2) + math.pow(blinkyY - pacmanY, 2))
    
    #Inky's X and Y coordinates based on his memory address.
    inkyX = api.peekCPU(0x0026) / 255.0
    inkyY = api.peekCPU(0x0028) / 255.0
    #Calculates the distance from inky to pacman based on their memory addresses.
    inkyDistance = math.sqrt( math.pow(inkyX - pacmanX, 2) + math.pow(inkyY - pacmanY, 2))

    #Clyde's X and Y coordinates based on his memory address.
    clydeX = api.peekCPU(0x002A) / 255.0
    clydeY = api.peekCPU(0x002C) / 255.0
    #Calculates the distance from cylde to pacman based on their memory addresses.
    clydeDistance = math.sqrt( math.pow(clydeX - pacmanX, 2) + math.pow(clydeY - pacmanY, 2))
    
    #nearestGhostDistance = math.min(pinkyDistance, blinkyDistance, inkyDistance, clydeDistance)
    deltaGhostDistance = nearestGhostDistance - lastNearestGhostDistance
    lastNearestGhostDistance = nearestGhostDistance
    
    timer = api.peekCPU(0x00DB)
    alive = timer == 0
    
    output = nn.fireNetwork([pacmanX, pacmanY,
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
    
    

api.addControllersListener(real_test_lol)
api.run()
