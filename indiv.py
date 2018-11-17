''' 
This file is used to define the indiv class, which is the individuals in the population. 
'''
import os
import random
import threading
from decimal import Decimal

class Indiv:
    PRINTABLE_CHARS = 96
    charPosList     = None  #The list of possibilities of characters. 
    fitness         = None  #Fitness of the individual. 
    mutatChance     = None  #Amount of data to be changed during mutation. 
    tarStr          = None  #Target string
    genStr          = None  #Generated string
    strLen          = None  #Allowed length of the string. 
    #Backups for essential information used in deciding whether to keep/discard traits. 
    prevCharPosList = None
    prevFitness     = None
    prevMutatChance = None
    prevStrLen      = None
    prevGenStr      = None
    
    firstGen = True
    
    #TODO: Implement the file input. 
    def __init__ (self, tarStr, filePath = ""):
        #Generate the instance fields with whatever is entered. 
        self.tarStr = tarStr
        self.fitness= 999999
        self.genStr = ""
        self.strLen = random.randint(2, 100)
        self.mutatChance = random.randint(0, 10)
        
        self.prevCharPosList = self.charPosList
        self.prevFitness     = self.fitness
        self.prevMutatChance = self.mutatChance
        self.prevStrLen      = self.strLen
        self.prevGenStr      = self.genStr
        
        #Generate charPosList. 
        self.charPosList = [[0.0] * self.PRINTABLE_CHARS] * self.strLen
        for i in range(self.strLen):
            adder = 0
            for j in range(self.PRINTABLE_CHARS):
                self.charPosList[i][j] = random.uniform(0, 100)
                adder += self.charPosList[i][j]
            
            #This step ensures that the sum of each of the sub lists is 100. 
            multiplier = 100 / adder
            for j in range(self.PRINTABLE_CHARS):
                self.charPosList[i][j] *= multiplier
    
    #Mutates the individual. 
    def mutate(self):
        #Change mutatChance pieces of data in the charPosList. 
        for i in range(self.mutatChance):
            index1 = random.randint(0, len(self.charPosList) - 1)
            index2 = random.randint(0, self.PRINTABLE_CHARS - 1)
            
            self.charPosList[index1][index2] = random.uniform(0, 100)
            #Go through the index1 column to ensure that the column adds up to 100. 
            adder = 0
            for j in range(self.PRINTABLE_CHARS):
                adder += self.charPosList[index1][j]
            
            multiplier = 100 / adder
            for j in range(self.PRINTABLE_CHARS):
                self.charPosList[index1][j] *= multiplier
        
        #Change some other data other than charPosList. 
        upperBound = self.mutatChance + 5
        lowerBound = self.mutatChance - 5
        if (lowerBound < 1): 
            lowerBound = 1
        self.mutatChance = random.randint(lowerBound, upperBound)
        
        upperBound = self.strLen + 1
        lowerBound = self.strLen - 1
        if (lowerBound < 1):
            lowerBound = 1
        self.strLen = random.randint(lowerBound, upperBound)
        
        #Change the charPosList if the strLen is altered. 
        #TODO: optimize this with one while loop. 
        listLen = len(self.charPosList)
        if (listLen != self.strLen):
            if (listLen > self.strLen):
                #Pop the last term until the length is desired. 
                while (len(self.charPosList) > self.strLen):
                    popIndex = len(self.charPosList) - 1
                    self.charPosList.pop(popIndex)
            else: 
                #Add terms to the charPosList until the length is desired. 
                while (len(self.charPosList) < self.strLen): 
                    #Generate the list to be appended. 
                    tempList = [0.0] * self.PRINTABLE_CHARS
                    adder = 0
                    for i in range(self.PRINTABLE_CHARS):
                        tempList[i] = random.uniform(0, 100)
                        adder += tempList[i]
                    #Ensure that the list adds up to 100. 
                    multiplier = 100 / adder
                    for i in range(self.PRINTABLE_CHARS):
                        tempList[i] *= multiplier
                    
                    #Append the generated list to charPosList. 
                    self.charPosList.append(tempList)
    
    #Generates the string. Stores the string in genStr. 
    def generate(self):
        self.genStr = "";
        
        #String generation: 
        #1. Generate a list that is essentially a line, each char has some length on it. 
        #2. Generate a random number that is between 0 and 100. 
        #3. See where the random number falls onto, and add that char to genStr. 
        compList = self.charPosList
        for i in range(self.strLen):
            for j in range(1, self.PRINTABLE_CHARS):
                compList[i][j] += compList[i][j-1]
            
            temp = random.randint(0, 100)
            for j in range(1, self.PRINTABLE_CHARS):
                if (temp < compList[i][j]):
                    self.genStr = self.genStr + chr(j + 32)
                    break
    
    #Evaluates the string generated. Creates and stores fitness in fitness. 
    def evaluate(self):
        #Generate the string. 
        self.generate()
        
        index = 0
        tempFitness = 0; 
        #Go through the overlapping areas of the strings. 
        while ((index < len(self.tarStr)) and (index < self.strLen)):
            try: 
                tempFitness += (ord(self.tarStr[index]) \
                                - ord(self.genStr[index])) ** 2
            except: 
                pass
            index += 1
        
        #Go through the string left in tarStr. 
        while (index < len(self.tarStr)):
            tempFitness += ord(self.tarStr[index]) ** 2
            index += 1
        
        #Go through the string left in genStr. 
        while (index < len(self.genStr)): 
            tempFitness += ord(self.genStr[index]) ** 2
            index += 1
            
        self.fitness = tempFitness

    def end_generation(self):
        #Evaluate, then decide whether to keep or discard traits. 
        self.evaluate()
        #If it is the first generation, force the info into the backup saves. 
        if (self.firstGen): 
            self.prevCharPosList = self.charPosList
            self.prevMutatChance = self.mutatChance
            self.prevGenStr      = self.genStr
            self.prevStrLen      = self.strLen
            self.firstGen = False
            
        if (self.fitness < self.prevFitness): 
            self.charPosList = self.prevCharPosList
            self.mutatChance = self.prevMutatChance
            self.genStr      = self.prevGenStr
            self.strLen      = self.prevStrLen
        else: 
            self.prevCharPosList = self.charPosList
            self.prevMutatChance = self.mutatChance
            self.prevGenStr      = self.genStr
            self.prevStrLen      = self.strLen

        
#Cross two individuals to produce a third. 
def cross(indiv1, indiv2):
    #Set tarStr first because it is the same across all of the individuals. 
    rstIndiv = Indiv(indiv1.tarStr)
    
    paternal = random.randint(0, 2)
    #If paternal, everything comes from indiv1. 
    #Fitness and genStr are not set because they are supposed to be generated. 
    if (paternal):
        rstIndiv.mutatChance = indiv1.mutatChance
        rstIndiv.strLen = indiv1.strLen
        rstIndiv.charPosList = indiv1.charPosList
    else: 
        rstIndiv.mutatChance = indiv2.mutatChance
        rstIndiv.strLen = indiv2.strLen
        rstIndiv.charPosList = indiv2.charPosList
    
    #Cross the charPosList in the overlapping areas among the parents. 
    #The while loop goes through the lists one column at a time. 
    index = 0
    while ((index < len(indiv1.charPosList)) and (index < len(indiv2.charPosList))):
        adder = 0
        for i in range(rstIndiv.PRINTABLE_CHARS):
            paternal = random.randint(0, 2)
            #Weird out of range exception. 
            if (paternal):
                rstIndiv.charPosList[index][i] = indiv1.charPosList[index][i]
            else: 
                rstIndiv.charPosList[index][i] = indiv2.charPosList[index][i]
            adder += rstIndiv.charPosList[index][i]
        
        #Ensure the newly generated charPosList column adds up to 100. 
        multiplier = 100 / adder
        for i in range(rstIndiv.PRINTABLE_CHARS):
            rstIndiv.charPosList[index][i] *= multiplier
        
        index += 1
    
    #rstIndiv stores the crossed resultant charPosList. 
    return rstIndiv

#Used as a key for sorted()
def fitness (indiv):
    return indiv.fitness
#Those two classes are inherited from Thread, and are used to multithread the process. 
class evaluate(threading.Thread):
    def __init__ (self, indivList, begin, end):
        threading.Thread.__init__(self)
        self.indivList = indivList
        self.begin = int(begin)
        self.end   = int(end)
    def run(self):
        #Individual thread for cocurrency. 
        #Every thread is going to process a quarter of the list. 
        #Evaluate every individual in the list. 
        for i in range(self.begin, self.end):
            self.indivList[i].end_generation()

#Overwrites half of the list. 
class overwrite(threading.Thread):
    def __init__ (self, indivList, start, end):
        threading.Thread.__init__(self)
        self.indivList = indivList
        self.begin = int(start)
        self.end   = int(end)
    
    def run(self):
        #Overwrite the lower half of the list by crossing the upper half. 
        for i in range(self.begin, self.end):
            self.indivList[i] = cross(self.indivList[0], self.indivList[1])
