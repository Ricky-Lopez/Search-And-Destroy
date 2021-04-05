
import queue
import random
import math
import time
import copy
import basicAgentOne
from random import randint

##data - class to be held in each cell. 
#isTarget = boolean which determines if the Target is there.
#probability = chances of agent NOT finding the Target GIVEN that the Target is indeed at this position; based on terrain specifications.
class data:
     def __init__(self, isTarget, probability) :
        self.isTarget = isTarget 
        self.probability = probability

## create_landscape
#creates the landscape given a dimension, and a terrain. Also randomly inserts target in a cell in the landscape.
def create_landscape(dim): #creates a landscape given dim dimension.
    landscape=[]
    for i in range(dim): #landscape creation
        c=[]
        for j in range(dim):
            rand = randint(1, 100)
            if rand in range(1, 25) : # Position is flat
                info = data(False, .1)
            elif rand in range(26, 50) : # Position is  hilly
                info = data(False, .3)
            elif rand in range(51, 75) : # Position is forested
                info = data(False, .7)
            else:                         # Position is a maze of caves
                info = data(False, .9)

            c.append(info)
        landscape.append(c)
    
    #Sets the target at a random location.
    randX = randint(0, dim-1)
    randY = randint(0, dim-1)

    landscape[randX][randY].isTarget = True

    return landscape



## print_landscape
#prints the real_landscape, with terrains and target. 
# -     Flat Terrain
# ~     Hilly Terrain
# ^     Forested Terrain
# }     Cave Terrain (I don't like this one)
def print_real_landscape(field,dim): #prints out the landscape BY THE PROPER COORDINATE CONVENTION (x,y) 
    columns = rows = 0
    print(" ",end="      ")
    for i in range(dim):
        if(columns < 10):
            print(columns, end="    ")
        elif(columns < 100):
            print(columns, end="   ")
        elif(columns < 1000):
            print(columns, end="  ")
        else:
            print(columns, end=" ")
        columns = columns + 1

    print("\n")
    for i in range(dim):
        if(rows < 10):
            print(rows, end="      ")
        elif(rows < 100):
            print(rows, end="     ")
        elif(rows < 1000):
            print(rows, end="    ")
        else:
            print(rows, end="   ")
        rows = rows + 1
        for j in range(dim):
            if(field[i][j].isTarget) : #Target is here
                print("T" , end="    ")
            elif (field[i][j].probability == .1) : #flat terrain
                print("-" , end="    ") 
            elif (field[i][j].probability == .3) : #hilly terrain
                print("~" , end="    ") 
            elif (field[i][j].probability == .7) : #forested terrain
                print("^" , end="    ") 
            else:                                  #cave terrain
                print("}" , end="    ") 
            
        print()
    print()

##search_position
#returns true if the target has not been found and the game should continue;
#returns false if the target has been found and that the game should end.
def search_position(landscape, pos) :
    rand = randint(1, 100)
    probNumber = landscape[pos[0]][pos[1]].probability * 100

    if(probNumber > rand) : #Terrain has bested the search
        return True
    else:                   #Terrain has been searched thoroughly
        return not(landscape[pos[0]][pos[1]].isTarget)
    
    

if __name__ == '__main__' :
    dim = int(input("Please enter the size of the landscape: "))
    landscape = create_landscape(dim)
    print_real_landscape(landscape, dim)
    whoPlays = input("Would you like to try and locate the target? y/n\n")
    whoPlays.lower()

    if(whoPlays == 'y' or whoPlays == 'yes'):
        whoPlays = True
    elif(whoPlays == 'n' or whoPlays == 'no'):
        print( basicAgentOne.basicAgentOne(landscape, dim))
        whoPlays = False
    else:
        print("I'm sorry, I don't think I understand. I'll just let the Agent play.", end="\n\n")
        whoPlays = False

    if(whoPlays) : #User gets to play
        print("\n******** SEARCH AND DESTROY *********\nRULES:\n\n1. Enter the position you would like to query in the format \"x,y\".\n2. To quit, enter \"q\".\n3. Have fun playing!\n\n")

        gameContinue = True
        turn = 0
        while(gameContinue) :
            if(turn > 0):
                print("Nothing was Found.\n")
            turn = turn + 1
            print("TURN " , turn)
            print
            user_input = input("Please enter the position you would like to check: ")
            user_input.lower()
            if(user_input == "q") :
                break
            else:
                try:
                    gameContinue = search_position(landscape, (int(user_input[0]), int(user_input[2])) )
                    print()
                except ValueError:
                    print("Invalid format. Please try again.\n")
    
        if(not(gameContinue)) :
            print("Congratulations! you have found the Target!")
    
        #TODO: Hide Target from the user landscape
