from indiv import *

def main():
    tgtStr = "Hello, World!"
    #Generate 100 individuals in the population with previously saved file. 
    indivList = []
    filePath = "data/"
    for i in range(100):
        filePath = "data/" + str(i) + ".txt"
        indivList.append(Indiv(tgtStr, filePath))
    
    generation = 0
    while (1):
        
        #Evaluate every individual in the list. 
        for i in range(len(indivList)):
            indivList[i].eval()
            indivList[i].end_generation()
        #Sort the list by fitness. 
        indivList.sort(key=fitness)
        #Print out the best fit of this generation. 
        print(generation, "\t|", indivList[0].genStr, "|\t", indivList[0].prevFitness, "\n")
        
        #Overwrite the lower half of the list by crossing the upper half. 
        for i in range(int(len(indivList) / 2), int(len(indivList))):
            indivList[i] = cross(indivList[i - int(len(indivList)/2)], indivList[i - int(len(indivList) / 2) + 1])
            
        generation += 1
        if (generation % 10000 == 0):
            save_progress(indivList)
        
if (__name__ == "__main__"):
    main()