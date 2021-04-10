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

# Searches the cell using the environment. Returns True is target is found. Returns False is Target isn't found    
def search_position(environment, pos) :
    rand = randint(1, 100) # Gets random # between 1 and 100
    searchCell = environment[pos[0]][pos[1]] # Grabs the cell position from the environment 
    target = searchCell.isTarget # Checks to see if the searched cell contains the target
    prob = searchCell.probability * 100 
    if(rand > prob): 
        return target
    else: #P(Taget not found in Cell | Target is in Cell)
        return False

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
    return currentHighest.probabilityOfContaning

class BFS_state:# hold the current state and the previous state
    def __init__(self, state, prev):
        self.state = state #current state
        self.prev = prev #previous states

def BFS(field, start_location, highestProb, dim): # Uses BFS to determine the shortest path from one state to another
    fringe = queue.Queue() #Fringe is a queue since its BFS (first come first out)
    closed = [] # holds the closed states
    shortest_path = [] # holds the current shortest path
    inFringe = []# holds the states that currently in the fringe
    start_state = BFS_state(start_location, 0)
    fringe.put(start_state)
    while(fringe.empty() == False): # loops while fringe isn't empty
        current_state = fringe.get()  #Pops state from fringe and makes current
        current = current_state.state
        i = current[0]
        j = current[1]
        if(field[i][j].probabilityOfContaning == highestProb): #if the end location is found on the fringe
            while(current != start_location):#Traces back through nodes to construct path
                shortest_path.append(current)
                current_state = current_state.prev # uses the BFS_state class to look for the previous state 
                current = current_state.state
            shortest_path.append(start_location)
            shortest_path.reverse() # reverses the path to make it go in correct orde
            return shortest_path
        else:
            i = current[0]
            j = current[1]
            if((i + 1) >= 0 and (i + 1) < dim ):   # Checks if the following state is in the maze range   
                    if(closed.count([i+1,j]) == 0 and inFringe.count([i+1,j]) == 0 ): #checks if the following state isn't already closed or in the fringe
                        new_state = BFS_state([i+1,j], current_state)# creates a new BFS_state and adds it the fringe
                        fringe.put(new_state)
                        inFringe.append([i+1,j])
            if((i - 1) >=0 and (i - 1) < dim):# Checks if the following state is in the maze range 
                    if(closed.count([i-1,j]) == 0 and inFringe.count([i-1,j]) == 0 ):#checks if the following state isn't already closed or in the fringe
                        new_state = BFS_state([i-1,j], current_state) # creates a new BFS_state and adds it the fringe
                        fringe.put(new_state)
                        inFringe.append([i-1,j])
            if((j + 1) >=0 and (j + 1) < dim):# Checks if the following state is in the maze range 
                    if(closed.count([i,j+1]) == 0 and inFringe.count([i,j+1]) == 0  ):#checks if the following state isn't already closed or in the fringe
                        new_state = BFS_state([i,j+1], current_state)# creates a new BFS_state and adds it the fringe
                        fringe.put(new_state)
                        inFringe.append([i,j+1]) 
            if((j - 1) >= 0 and (j - 1) < dim):# Checks if the following state is in the maze range 
                    if(closed.count([i,j-1]) == 0 and inFringe.count([i,j-1]) == 0):#checks if the following state isn't already closed or in the fringe
                        new_state = BFS_state([i,j-1], current_state)# creates a new BFS_state and adds it the fringe
                        fringe.put(new_state)
                        inFringe.append([i,j-1])
            closed.append(current)  #puts current state in closed after generating valid children
   
 
    
def basicAgentOne(environment, dim, startingPosition):

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
        
        #printField(field, dim) # Prints the field
        
        time = time + 1
        
        highestProb = findHighestProbability(field, dim, currentCell) # Gets the highest probability of the field
        
        if(currentCell.probabilityOfContaning == highestProb):
            
            found = search_position(environment, currentCell.position) # Agent searches current cell
        
            if(found == True): # If target was found, return time
                return time
            else:
                #Else, the probability of the cells in the field are updated
                print("Agent searched cell:", currentCell.position)
                updateProbability(field, dim,  currentCell) 
        else:
            
            path = BFS(field, currentCell.position, highestProb, dim) # Calculates the path to the highest probability
            
            nextStep = path[1] # Gets the next step the agents takes to thr highest probability
            
            X = nextStep[0]
            Y = nextStep[1]
            
            #Moves the Agent to the next Step
            print("Agent moved to cell:", nextStep)
            currentCell.agent = False
            currentCell = field[X][Y]
            currentCell.agent = True
        
        
        
        
    
    
    
    
    
   
    
    
    
   
    
    
    