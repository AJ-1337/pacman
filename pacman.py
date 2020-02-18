import sys
import nintaco
import math

nintaco.initRemoteAPI("localhost", 9999)
api = nintaco.getAPI()

def test():
    pacmanX = api.peekCPU(0x001A)
    pacmanY = api.peekCPU(0x001C)
    
    pinkyX = api.peekCPU(0x0022)
    pinkyY = api.peekCPU(0x0024)
    distance = math.sqrt(math.pow(pinkyX - pacmanX, 2) + math.pow(pinkyY - pacmanY, 2))
    print(distance)
    

api.addFrameListener(test)
api.run()