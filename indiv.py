''' 
This file is used to define the indiv class, which is the individuals in the population. 
'''
import os
import random
from decimal import Decimal

class Indiv:
    random.seed()
    
    charPos   = [0.0] * 96      #Possibility to generate each printable char. Stored in a number between 0 to 100. 
    prevCharPos = charPos       #Stores the previous charPos as reference
    genStr    = ""              #Generated string. 
    chanceMut = 0               #Amount of possibilities allowed to mutate. 
    lenStr    = 10              #Allowed length of the generated string. 
    prevLenStr=lenStr           #Reference for length allowance. 
    tarStr    = ""              #Target string. 
    fitness   = 100000000       #Set to a trivial large value to make sure the first mutation is saved.  
    prevFitness = fitness       #Fitness reference. If the current fitness is larger than the previoud one, do not write the mutated value in. 
    
    #Constructor.
    def __init__(self, tarStr = "", filePath = ""):
        dataFileExistence = os.path.isfile(filePath)
        #If a filePath is inputed, look into the file. 
        #1st line: chanceMut. 
        #2nd line: tarStr. 
        #3rd line: lenStr. 
        #After: a possibility number ever line. 
        dataCache = []  #dataCache used to store the split data. 
        
        if (dataFileExistence):
            #opens the file and reads into a string, then closes the file. 
            with open(filePath, "r") as inputFile: 
                fileData = inputFile.read()
            
            #Split the file for a string list of data. 
            dataCache= fileData.split("\n")
            
            #Take care of the first two values. 
            self.chanceMut = int(dataCache[0])
            self.tarStr    = dataCache[1]
            self.lenStr    = int(dataCache[2])
            #Go through dataCache and assign the values to the possibility array.
            for i in range(3, len(dataCache)-1):
                self.charPos[i-3] = float(dataCache[i])
        else: 
            #If a filePath is invalid, generate new list of possibilities. 
            #Check if tarStr is valid. If not, raise error. 
            if (not tarStr):
                raise ValueError("Invalid target phrase.")
            
            for i in range(96):
                self.charPos[i] = random.uniform(0, 100)
            
        #Set target string. 
        self.tarStr = tarStr
            
    #eval(): Generates a string according to the possibilities and allowed chars, then compares that with tarStr. 
    def eval(self):
        self.fitness= 0
        self.genStr = ""    #Clears the previously generated string. 
        randomCache = 0     #Stores a random number. If the number is smaller than the stored possibility value, the char is added to the generated string. 
        
        #String generation. 
        for i in range(self.lenStr):
            #Go through the possibility string. 
            for i in range(96):
                randomCache = random.randint(0, 100)
                if (randomCache <= self.charPos[i]):
                    #If a char is generated, add that to the end of the string, break. 
                    self.genStr = self.genStr + chr(i + 32);
                    break
        
        cycleLength = min(self.lenStr, len(self.tarStr))
        #Fitness evaluation. 
        #Parse through the part in which both strings have value. 
        for i in range(cycleLength):
            #Add the difference between target string char and generated string char. 
            #the closer the generated string is to the target, the smaller fitness score will be. 
            self.fitness += abs(ord(self.tarStr[i]) - ord(self.genStr[i]))
        
        #If there are leftover letters in either tarStr or genStr, add them to fitness. 
        if (len(self.genStr) > cycleLength):
            for i in range(cycleLength, len(self.genStr)):
                self.fitness += ord(self.genStr[i])
        elif (len(self.tarStr) > cycleLength):
            for i in range(cycleLength, len(self.tarStr)):
                self.fitness += ord(self.tarStr[i])
        
            
            
    #mutate(): Mutates the individual. Changes some possibilities, changes lenStr. 
    def mutate(self):
        self.lenStr = random.randint(self.lenStr - 1, self.lenStr + 1) if self.lenStr > 1 else random.randint(0, self.lenStr + 1)
        
        self.chanceMut = random.randint(self.chanceMut - 5, self.chanceMut + 5) if self.chanceMut > 5 else random.randint(0, self.chanceMut + 5)
        
        randIndex = 0       #The index of the value that is to be changed. 
        possibilityCache = 0
        for i in range(self.chanceMut):
            randIndex = random.randint(0, 95)
            '''
            upperCache = int(self.charPos[randIndex]+5)
            lowerCache = int(self.charPos[randIndex]-5)
            if (self.charPos[randIndex] >= 5): 
                possibilityCache = random.randint(lowerCache, upperCache)
            elif (self.charPos[randIndex]+5 >= 95): 
                possibilityCache = random.randint(int(lowerCache, self.charPos[randIndex]))
            elif (self.charPos[randIndex] < 5):
                possibilityCache = random.randint(0, upperCache)
            '''
            self.charPos[randIndex] = random.uniform(0, 100)
    
    #end_generation: Decide whether the current generation is worth keeping. 
    def end_generation(self):
        #If the current fitness value is less than the previous one, save the current values. 
        #otherwise discard current values. 
        if (self.fitness < self.prevFitness):
            self.prevCharPos = self.charPos
            self.prevFitness = self.fitness
            self.prevLenStr  = self.lenStr
        else: 
            self.charPos = self.prevCharPos
            self.lenStr  = self.prevLenStr
            
#Takes in a Indiv object, returns the fitness. Use alongside built-in sort function. 
def fitness(indiv):
    return indiv.fitness

#cross: Takes in two indiv objects, crosses the possibility list. 
#lenStr, chanceMut is randomly chosen from one of the parents. 
#returns an indiv object. 
def cross(indiv1, indiv2):
    #define paternal as from indiv1. 
    #Make new Indiv object with the same tarStr. 
    rstIndiv = Indiv(indiv1.tarStr)
    paternal = random.randint(0, 1)
    if (paternal):
        rstIndiv.lenStr    = indiv1.lenStr
        rstIndiv.chanceMut = indiv1.chanceMut
    else: 
        rstIndiv.lenStr    = indiv2.lenStr
        rstIndiv.chanceMut = indiv2.chanceMut
    
    #Cross the possibilities. 
    for i in range(len(rstIndiv.charPos)):
        paternal = random.randint(0, 1)
        if (paternal):
            rstIndiv.charPos[i] = indiv1.charPos[i]
        else: 
            rstIndiv.charPos[i] = indiv2.charPos[i]
    
    #Mutate and evaluate before returning. 
    rstIndiv.mutate()
    rstIndiv.eval()
    return rstIndiv

#Saves the current weight data. 
def save_progress(indivList):
    for i in range(len(indivList)):
        fileName = "data/" + str(i) + ".txt"
        endStr = ""
        try: 
            os.remove(fileName)
        except: 
            pass
        with open(fileName, "w+") as saveFile: 
            endStr = endStr + str(indivList[i].chanceMut) + "\n"
            endStr = endStr + str(indivList[i].tarStr) + "\n"
            endStr = endStr + str(indivList[i].lenStr) + "\n"
            for j in range(len(indivList[i].charPos)):
                endStr = endStr + str(indivList[i].charPos[j]) + "\n"
            
            saveFile.write(endStr)
