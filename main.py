from indiv import *


#main
def main():
    random.seed()
    tgtStr = "Hello, World!"
    populationSize = 1000
    populationList = [None]
    THREAD_COUNT = 4
    generation = 0
    
    populationList.pop(0)
    
    for i in range(populationSize):
        populationList.append(Indiv(tgtStr))
     
    #TODO: Add multi-threading. 
    while (1):
        generation += 1
        
        for i in range(populationSize):
            populationList[i].mutate()
            populationList[i].end_generation()
        
        populationList.sort(key=fitness)
        
        bestFit = populationList[0]
        print (generation, "\t|", bestFit.genStr, "|\t", bestFit.fitness, "\n")
        
        start = int(populationSize / 2)
        end   = populationSize
        for i in range(start, end):
            populationList[i] = cross(populationList[0], populationList[i - start])
        
if (__name__ == "__main__"):
    main()

