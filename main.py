import nintaco
import evolver as Evolver

populationSize = input("Enter the population size: ")
mutationRate = input("Enter the mutation rate (0-1): ")
maxGenerations = input("How many generations should be ran before toggling the AI off (0 for unlimited): ")
showResults = str(raw_input("Show results report after the AI is toggled off (y/n): "))
showResults = showResults == "y" or showResults == "Y"

nintaco.initRemoteAPI("localhost", 9999)
api = nintaco.getAPI()
evolver = Evolver.Evolver(api, populationSize = populationSize, mutationRate = mutationRate, maxGenerations = maxGenerations, showResults = showResults)
api.addFrameListener(evolver.playGame)
api.addAccessPointListener(evolver.onLifeCountChanged, nintaco.PostWrite, 0x0067)
api.run()