import queue
import random
import math
import time
import copy
import environment


from random import randint


class agentKnowledgedata:
     def __init__(self, prosition, terrain, probability, probabilityOfContaning, Observations, agent) : 
        self.prosition = prosition
        self.terrain = terrain
        self.probability = probability
        self.probabilityOfContaning = probabilityOfContaning
        self.Observations = Observations
        self.agent = agent

def setField(environment, dim):
    totalCells = dim * dim
    Initialprob = 1 / totalCells
    field = []
    for i in range(dim):
        c= []
        for j in range(dim):
            environmentProsition = environment[i][j]
            if(environmentProsition.probability == .1):
                cellData = agentKnowledgedata([i,j],'-', .1, Initialprob, 0 , False)
            elif(environmentProsition.probability == .3):
                cellData = agentKnowledgedata([i,j],'~', .3, Initialprob, 0 , False)
            elif(environmentProsition.probability == .7):
                cellData = agentKnowledgedata([i,j],'^', .7, Initialprob, 0 , False)
            else:
                cellData = agentKnowledgedata([i,j],'}', .9, Initialprob, 0 , False)
            c.append(cellData)
        field.append(c)
    return field

def printField(field, dim):
    for i in range(dim):
        for j in range(dim):
            if(field[i][j].agent == False):
                print(field[i][j].terrain, "{:.2f}".format(field[i][j].probabilityOfContaning) , end = "     ")
            else:
                print('A', field[i][j].terrain, "{:.2f}".format(field[i][j].probabilityOfContaning) , end = "   ")
        print()
    print()
    
def search_position(environment, pos) :
    rand = randint(1, 100)
    searchCell = environment[pos[0]][pos[1]] 
    target = searchCell.isTarget
    prob = searchCell.probability * 100 
    if(rand > prob):
        return target
    else:
        return False

def updateProbability(field, dim,  currentCell):
    totalCells = dim * dim
    probability = currentCell.probability
    probabilityContaning = currentCell.probabilityOfContaning
    position = currentCell.prosition
    X = position[0]
    Y = position[1]
    newProbabilityContaning = probabilityContaning * probability
    leftOver = probabilityContaning - newProbabilityContaning
    addedProbability = leftOver / (totalCells - 1)
    currentCell.probabilityOfContaning = newProbabilityContaning
    
    for i in range(dim):
        for j in range(dim):
            if(X != i or Y != j):
                   field[i][j].probabilityOfContaning = field[i][j].probabilityOfContaning + addedProbability
    return  
       

def basicAgentOne(environment, dim):
    
    
    field = setField(environment,dim)
    printField(field, dim)
    
    X = randint(0, dim-1)
    Y = randint(0, dim-1)
    
    currentCell = field[X][Y]
    currentCell.agent = True
    print("added Agent")
    
    
    time = 0
    
    while(1):
        
        time = time + 1
        
        printField(field, dim)
        
        currentPropabilty = currentCell.probabilityOfContaning
        
        X = currentCell.prosition[0]
        Y = currentCell.prosition[1]
        
        changed = False
        
        #find surrounding cells
        if((X+1) < dim):
            if(field[X+1][Y].probabilityOfContaning > currentPropabilty):
                currentCell.agent = False
                currentCell = field[X+1][Y]
                currentCell.agent = True
                changed = True
        if((X-1) >= 0):
            if(field[X-1][Y].probabilityOfContaning > currentPropabilty):
                currentCell.agent = False
                currentCell = field[X-1][Y]
                currentCell.agent = True
                changed = True
        if((Y+1) < dim):
            if(field[X][Y+1].probabilityOfContaning > currentPropabilty):
                currentCell.agent = False
                currentCell = field[X][Y+1]
                currentCell.agent = True
                changed = True 
        if((Y-1) >= 0):
            if(field[X][Y-1].probabilityOfContaning > currentPropabilty):
                currentCell.agent = False
                currentCell = field[X][Y-1]
                currentCell.agent = True
                changed = True     
            
        if(changed == False):
            
            found = search_position(environment, currentCell.prosition)
        
            if(found == True):
                return time
            else:
                print("Agent searched cell:", currentCell.prosition)
                updateProbability(field, dim,  currentCell)
        else:
            print("Agent Moved to cell:" , currentCell.prosition)
            
        
    
    
    
    
    
   
    
    
    
   
    
    
    