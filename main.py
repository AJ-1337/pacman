import nintaco
import evolver as Evolver

nintaco.initRemoteAPI("localhost", 9999)
api = nintaco.getAPI()
evolver = Evolver.Evolver(api, populationSize = 100, mutationRate = 0.2)
api.addFrameListener(evolver.playGame)
api.addAccessPointListener(evolver.onLifeCountChanged, nintaco.PostWrite, 0x0067)
api.run()