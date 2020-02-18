import sys
import nintaco
import math
import neuralNetwork

nintaco.initRemoteAPI("localhost", 9999)
api = nintaco.getAPI()

nn = neuralNetwork.NeuralNetwork(4, 4)

def test():
    pacmanX = api.peekCPU(0x001A) / 255.0
    pacmanY = api.peekCPU(0x001C) / 255.0
    
    pinkyX = api.peekCPU(0x0022) / 255.0
    pinkyY = api.peekCPU(0x0024) / 255.0
    print(pacmanX, pacmanY, pinkyX, pinkyY)
    nn.clearNeurons()
    output = nn.fireNetwork([pacmanX, pacmanY, pinkyX, pinkyY])
    for o in output:
        print(o)
    m = max(output)
    if output[0] >= m:
        api.writeGamepad(0, 4, True) # Gamepad 0, 4 = up, True = pressed
    elif output[1] >= m:
        api.writeGamepad(0, 5, True) # down
    elif output[2] >= m:
        api.writeGamepad(0, 6, True) # left
    elif output[3] >= m:
        api.writeGamepad(0, 7, True) # right

api.addFrameListener(test)
api.run()