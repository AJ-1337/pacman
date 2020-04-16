import pytest
import neuralNetwork as nn
import evolver as Evolver
import nintaco

#Testing requirements


def test_sendControllerInput():
    nintaco.initRemoteAPI("localhost", 9999)
    api = nintaco.getAPI()
    evolver = Evolver.Evolver(api)
    exit()
    def writeAndRead():
        print("?")
        evolver.writeGamepad(Evolver.GAMEPAD_START, True)
        assert api.readGamepad(0, Evolver.GAMEPAD_START)
        pytest.exit()
    
    api.addFrameListener(writeAndRead)

    api.run()
    

#Bonus / supplementary tests for additional coverage
def test_sigmoid():
    assert nn.sigmoid(0) == pytest.approx(0.5)