import queue
import random
import math
import time
import copy
import environment


from random import randint

##agentKnowledgedata - class to be held in each cell. 
class agentKnowledgedata:
     def __init__(self, position, terrain, probability, probabilityOfContaning, agent) : 
        self.position = position #Holds the position of the cell
        self.terrain = terrain #Holds the terrain type of the cell
        self.probability = probability #Holds the probability of Target not found in cell while target is in Cell
        self.probabilityOfContaning = probabilityOfContaning #Holds the probability of the cell containing the target
        self.agent = agent #If the Agent is currently at the cell

#Sets up the field and establishes a knowledgedata for each cell given the environment
def setField(environment, dim):
    totalCells = dim * dim
    Initialprob = 1 / totalCells # P(Target in Cell) = 1 / # of cells
    field = []
    for i in range(dim):
        c= []
        for j in range(dim):
            environmentProsition = environment[i][j]
            if(environmentProsition.probability == .1): #If the cell is flat
                cellData = agentKnowledgedata([i,j],'-', .1, Initialprob, False)
            elif(environmentProsition.probability == .3): #if the cell is hilly
                cellData = agentKnowledgedata([i,j],'~', .3, Initialprob, False)
            elif(environmentProsition.probability == .7): #if the cell is forested
                cellData = agentKnowledgedata([i,j],'^', .7, Initialprob, False)
            else: # if the cell is a maze of caves
                cellData = agentKnowledgedata([i,j],'}', .9, Initialprob, False)
            c.append(cellData)
        field.append(c)
    return field

# Prints out the field that the agent sees. Doesn't contain the target. Used only for testing
def printField(field, dim):
    for i in range(dim):
        for j in range(dim):
            if(field[i][j].agent == False):
                print(field[i][j].terrain, "{:.2f}".format(field[i][j].probabilityOfContaning) , end = "     ")
            else:
                print('A', field[i][j].terrain, "{:.2f}".format(field[i][j].probabilityOfContaning) , end = "   ")
        print()
    print()

#Determines where the Target is, and figures out Manhattan Distance of the agent and Target.
def manhattan_distance(environment, pos, dim):
    for i in range(dim):
        for j in range(dim):
            if (environment[i][j].isTarget): #Target has been located
                            targetPos = [i, j]

    xDiff = math.sqrt((targetPos[0] - pos[0]) ** 2)
    yDiff = math.sqrt((targetPos[1] - pos[1]) ** 2)

    if((xDiff + yDiff) < 5) :
        return True
    
    return False


# Searches the cell using the environment. Returns 1 if target is found. Returns 0 is Target isn't found. Returns 2 if Target isn't found, but is within a manhattan distance of 5.  
def search_position(environment1, pos) :
    
    
    rand = randint(1, 100) # Gets random # between 1 and 100
    searchCell = environment1[pos[0]][pos[1]] # Grabs the cell position from the environment 
    target = searchCell.isTarget # Checks to see if the searched cell contains the target
    prob = searchCell.probability * 100 

    if(target):
        if(rand > prob): 
            return 1 #Returns 1 if the target has been found!
    environment.move_target(environment1, len(environment1))
    isClose = manhattan_distance(environment1, pos, len(environment1))
    if(isClose):
        return 2 #Not found but within a Manhattan-Distance of 5
    return 0


# Updates all the cells and the probability it contains a target
def updateProbability(field, dim,  currentCell):
    #Sets all the info needed
    totalCells = dim * dim
    probability = currentCell.probability
    probabilityContaning = currentCell.probabilityOfContaning
    position = currentCell.position
    X = position[0]
    Y = position[1]
    #Bayes Theorem
    newProbabilityContaning = ((probabilityContaning * probability) / ((1-probabilityContaning) + (probabilityContaning * probability)))
    currentCell.probabilityOfContaning = newProbabilityContaning # Sets the new probability to the cells probability of Containing
    #leftOver = probabilityContaning - newProbabilityContaning #Gets the probability left over when setting the new probability
    #addedProbability = leftOver / (totalCells - 1) # Gets the amount of probability to be added to all the other cells
    
    #Updates all the other cells
    for i in range(dim):
        for j in range(dim):
            if(X != i or Y != j):
                   field[i][j].probabilityOfContaning = ((field[i][j].probabilityOfContaning * 1) / ((1-probabilityContaning) + (probabilityContaning * probability)))
    return  

def findHighestProbability(field, dim, currentPosition):
    currentHighest = currentPosition
    for i in range(dim):
        for j in range(dim):
            if(currentHighest.probabilityOfContaning < field[i][j].probabilityOfContaning):
                currentHighest = field[i][j]
    return currentHighest
    
def improvedAgent(environment, dim, startingPosition):

    field = setField(environment,dim) # Establishes a field for the Agent
    printField(field, dim)
    
    X = startingPosition[0]
    Y = startingPosition[1]
    
    currentCell = field[X][Y]
    #currentCell = field[0][0]
    currentCell.agent = True # Added a agent to the field
    print("added Agent")
    
    
    time = 0 # Holds the time ( 'total distance traveled + 'number of searches')
    
    while(1):
        
        time = time + 1
        
        #printField(field, dim)
        
        currentPropabilty = currentCell.probabilityOfContaning # Holds the probability of the current cell containing a target
        
        X = currentCell.position[0]
        Y = currentCell.position[1]
        
        changed = False # Determines if the agents changed cells
        
        #find surrounding cells
        if((X+1) < dim): #check the cell below the current
            if(field[X+1][Y].probabilityOfContaning > currentPropabilty):
                #If the below cell has a higher probability, the agent moves
                currentCell.agent = False
                currentCell = field[X+1][Y]
                currentPropabilty = currentCell.probabilityOfContaning
                currentCell.agent = True
                changed = True
        if((X-1) >= 0): #check the cell above the current
            if(field[X-1][Y].probabilityOfContaning > currentPropabilty):
                #If the above cell has a higher probability, the agent moves
                currentCell.agent = False
                currentCell = field[X-1][Y]
                currentPropabilty = currentCell.probabilityOfContaning
                currentCell.agent = True
                changed = True
        if((Y+1) < dim):#check the cell right of the current
            if(field[X][Y+1].probabilityOfContaning > currentPropabilty):
                #If the right cell has a higher probability, the agent moves
                currentCell.agent = False
                currentCell = field[X][Y+1]
                currentPropabilty = currentCell.probabilityOfContaning
                currentCell.agent = True
                changed = True 
        if((Y-1) >= 0):#check the cell left of the current
            if(field[X][Y-1].probabilityOfContaning > currentPropabilty):
                #If the left cell has a higher probability, the agent moves
                currentCell.agent = False
                currentCell = field[X][Y-1]
                currentPropabilty = currentCell.probabilityOfContaning
                currentCell.agent = True
                changed = True     
            
        if(changed == False): # if the agent never changed cells, the agent will search its current cell
            
            found = search_position(environment, currentCell.position) # Agent searches current cell
        
            if(found == 1): # If target was found, return agound of time
                print("Target has been found!")
                return time
            elif(found == 0): #Target was not found, and is not within a Manhattan distance of 5 from the Agent
                #Else, the probability of the cells in the field are updated
                print("Agent searched cell:", currentCell.position)
                updateProbability(field, dim,  currentCell)
            elif(found == 2): #Target was not found, but is within a Manhattan distance of 5 from the Agent.
                print("Target is within 5 unit spaces of the agent.")
                #TODO: Write new probability function for this situation!
            else:
                print("Agent Moved to cell:" , currentCell.position)
            
        
    
    
    
    
    
   