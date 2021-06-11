
from Agent import Agent
from StateAI import StateAI
import random
import turtle

class World():
    # Tile Structure
    class __Tile:
        pit = False;
        wumpus = False;
        gold = False;
        breeze = False;
        stench = False;

    def __init__(self, debug=False):
        # Operation Flags
        self.__debug = debug

        # Agent Initialization
        self.__goldLooted = False
        self.__hasArrow = True
        self.__bump = False
        self.__scream = False
       
        self.__agentDir = 0
        self.__agentX = 0
        self.__agentY = 0
        self.__lastAction = Agent.Action.CLIMB
        self.__goldExist = False
        self.__wumpusExist = False
        self.__pitExist = False

        self.__agent = StateAI()

        self.__colDimension = 4
        self.__rowDimension = 4
        self.__board = [[self.__Tile() for j in range(self.__colDimension)] for i in range(self.__rowDimension)]
        self.__addFeatures()


    def run(self):

        while True:
            caution = 0
            if self.__debug:
                self.__printWorldInfo()

                if not self.__bump :
                  self.__agent.getXY(self.__agentX+1,self.__agentY+1)

                input("Press ENTER to continue...")
      

            # Get the move
            self.__lastAction = self.__agent.getAction(
                self.__board[self.__agentX][self.__agentY].stench,
                self.__board[self.__agentX][self.__agentY].breeze,
                self.__board[self.__agentX][self.__agentY].gold,
                self.__bump,
                self.__scream
            )

            # Make the move
            self.__bump = False
            self.__scream = False

            if self.__lastAction == Agent.Action.TURN_LEFT:
                self.__agentDir -= 1
                if (self.__agentDir < 0):
                    self.__agentDir = 3

            elif self.__lastAction == Agent.Action.TURN_RIGHT:
                self.__agentDir += 1
                if self.__agentDir > 3:
                    self.__agentDir = 0

            elif self.__lastAction == Agent.Action.FORWARD:
                if self.__agentDir == 0 and self.__agentX + 1 < self.__colDimension:
                    self.__agentX += 1
                elif self.__agentDir == 1 and self.__agentY - 1 >= 0:
                    self.__agentY -= 1
                elif self.__agentDir == 2 and self.__agentX - 1 >= 0:
                    self.__agentX -= 1
                elif self.__agentDir == 3 and self.__agentY + 1 < self.__rowDimension:
                    self.__agentY += 1
                else:
                    self.__bump = True

                if self.__board[self.__agentX][self.__agentY].pit or self.__board[self.__agentX][self.__agentY].wumpus:
                    self.__agent.getXY(self.__agentX+1, self.__agentY+1)
                    if self.__board[self.__agentX][self.__agentY].pit:
                        caution = 1 
                    if self.__board[self.__agentX][self.__agentY].wumpus:  
                        caution = 2 
                    if self.__board[self.__agentX][self.__agentY].pit and self.__board[self.__agentX][self.__agentY].wumpus:
                        caution = 3 
                    self.__agent.getPercept(
                    self.__board[self.__agentX][self.__agentY].stench,
                    self.__board[self.__agentX][self.__agentY].breeze,
                    self.__board[self.__agentX][self.__agentY].gold,
                    self.__bump,
                    self.__scream,
                    caution
                    )
                    caution = 0
                    self.__agent.setHome(self.__agentX+1,self.__agentY+1,self.__board[self.__agentX][self.__agentY].pit,self.__board[self.__agentX][self.__agentY].wumpus)
                    self.__agentX = 0
                    self.__agentY = 0

                    if self.__debug:
                        self.__printWorldInfo()


                

            elif self.__lastAction == Agent.Action.SHOOT:

                if self.__hasArrow:
                    self.__hasArrow = False
               
                    if self.__agentDir == 0:
                        for x in range(self.__agentX, self.__colDimension):
                            if self.__board[x][self.__agentY].wumpus:
                                self.__board[x][self.__agentY].wumpus = False
                                self.__board[x][self.__agentY].stench = False
                                self.__scream = True

                        self.__board[self.__agentX][self.__agentY].stench = False
                        if self.__agentX+2 < self.__colDimension and self.__agentY < self.__rowDimension:
                            self.__board[self.__agentX+2][self.__agentY].stench = False
                        if self.__agentX+1 < self.__colDimension and self.__agentY+1 < self.__rowDimension:
                            self.__board[self.__agentX+1][self.__agentY+1].stench = False
                        if self.__agentX + 1 < self.__colDimension and self.__agentY - 1 < self.__rowDimension:
                            self.__board[self.__agentX + 1][self.__agentY - 1].stench = False

                    elif self.__agentDir == 1:
                        for y in range(self.__agentY, -1, -1):
                            if self.__board[self.__agentX][y].wumpus:
                                self.__board[self.__agentX][y].wumpus = False
                                self.__board[self.__agentX][y].stench = False
                                self.__scream = True

                        self.__board[self.__agentX][self.__agentY].stench = False
                        if self.__agentX< self.__colDimension and self.__agentY-2 < self.__rowDimension:
                            self.__board[self.__agentX][self.__agentY-2].stench = False
                        if self.__agentX + 1 < self.__colDimension and self.__agentY -1 < self.__rowDimension:
                            self.__board[self.__agentX + 1][self.__agentY - 1].stench = False
                        if self.__agentX - 1 < self.__colDimension and self.__agentY - 1 < self.__rowDimension:
                            self.__board[self.__agentX - 1][self.__agentY - 1].stench = False

                    elif self.__agentDir == 2:
                        for x in range(self.__agentX, -1, -1):
                            if self.__board[x][self.__agentY].wumpus:
                                self.__board[x][self.__agentY].wumpus = False
                                self.__board[x][self.__agentY].stench = False
                                self.__scream = True

                        self.__board[self.__agentX][self.__agentY].stench = False
                        if self.__agentX - 1 < self.__colDimension and self.__agentY + 1 < self.__rowDimension:
                            self.__board[self.__agentX-1][self.__agentY +1].stench = False
                        if self.__agentX - 1 < self.__colDimension and self.__agentY - 1 < self.__rowDimension:
                            self.__board[self.__agentX -1][self.__agentY - 1].stench = False
                        if self.__agentX -2 < self.__colDimension and self.__agentY < self.__rowDimension:
                            self.__board[self.__agentX - 2][self.__agentY].stench = False

                    elif self.__agentDir == 3:
                        for y in range(self.__agentY, self.__rowDimension):
                            if self.__board[self.__agentX][y].wumpus:
                                self.__board[self.__agentX][y].wumpus = False
                                self.__board[self.__agentX][y].stench = False
                                self.__scream = True

                        self.__board[self.__agentX][self.__agentY].stench = False
                        if self.__agentX - 1 < self.__colDimension and self.__agentY + 1 < self.__rowDimension:
                            self.__board[self.__agentX - 1][self.__agentY + 1].stench = False
                        if self.__agentX + 1 < self.__colDimension and self.__agentY + 1 < self.__rowDimension:
                            self.__board[self.__agentX +1][self.__agentY + 1].stench = False
                        if self.__agentX< self.__colDimension and self.__agentY + 2 < self.__rowDimension:
                            self.__board[self.__agentX][self.__agentY+2].stench = False



            elif self.__lastAction == Agent.Action.GRAB:
                if self.__board[self.__agentX][self.__agentY].gold:
                    self.__board[self.__agentX][self.__agentY].gold = False
                    self.__goldLooted = True

            elif self.__lastAction == Agent.Action.CLIMB:
                if self.__agentX == 0 and self.__agentY == 0:
                    self.__agent.finish_ment()
                    if self.__debug:
                        self.__printWorldInfo()
                    return True

            self.__agent.getPercept(
                self.__board[self.__agentX][self.__agentY].stench,
                self.__board[self.__agentX][self.__agentY].breeze,
                self.__board[self.__agentX][self.__agentY].gold,
                self.__bump,
                self.__scream,
                caution
            )

            

        

            
        return False

  
    #World Generation Functions
    def __addFeatures(self):

        # Generate pits
        while not self.__pitExist:
            for pr in range(self.__rowDimension):
                for pc in range(self.__colDimension):
                    if (pc != 0 or pr != 0) and self.__randomInt(100) < 15:
                        if not ((pc == 0 and pr == 1) or (pc == 1 and pr == 0)) and not self.__pitExist:
                            self.__addPit(pc, pr)
                            self.__pitExist = True

        # Generate wumpus
        while not self.__wumpusExist:
            for wr in range(self.__rowDimension):
                for wc in range(self.__colDimension):
                    if (wc != 0 or wr != 0) and self.__randomInt(100) < 15:
                        if not ((wc == 0 and wr == 1) or (wc == 1 and wr == 0)) and not self.__wumpusExist:
                            self.__addWumpus(wc, wr)
                            self.__wumpusExist = True

        # Generate gold
        while not self.__goldExist:
            for gr in range(self.__rowDimension):
                for gc in range(self.__colDimension):
                    if (gc != 0 or gr != 0) and self.__randomInt(100) < 15:
                        if not ((gc == 0 and gr == 1) or (gc == 1 and gr == 0)):
                            if not (self.__board[gc][gr].pit or self.__board[gc][gr].wumpus) and not self.__goldExist:
                                self.__addGold(gc, gr)
                                self.__goldExist = True

    def __addPit(self, c, r):
        if self.__isInBounds(c, r):
            self.__board[c][r].pit = True
            self.__addBreeze(c + 1, r)
            self.__addBreeze(c - 1, r)
            self.__addBreeze(c, r + 1)
            self.__addBreeze(c, r - 1)

    def __addWumpus(self, c, r):
        if self.__isInBounds(c, r):
            self.__board[c][r].wumpus = True
            self.__addStench(c + 1, r)
            self.__addStench(c - 1, r)
            self.__addStench(c, r + 1)
            self.__addStench(c, r - 1)

    def __addGold(self, c, r):
        if self.__isInBounds(c, r):
            self.__board[c][r].gold = True

    def __addStench(self, c, r):
        if self.__isInBounds(c, r):
            self.__board[c][r].stench = True

    def __addBreeze(self, c, r):
        if self.__isInBounds(c, r):
            self.__board[c][r].breeze = True

    def __isInBounds(self, c, r):
        return c < self.__colDimension and r < self.__rowDimension and c >= 0 and r >= 0

   
    #World Printing Functions
    def __printWorldInfo(self):
        self.__printBoardInfo()
        self.__printAgentInfo()

    def __printBoardInfo(self):
        for r in range(self.__rowDimension - 1, -1, -1):
            for c in range(self.__colDimension):
                self.__printTileInfo(c, r)
            print("")
            print("")

    def __printTileInfo(self, c, r):
        tileString = ""

        if self.__board[c][r].pit:    tileString += "P"
        if self.__board[c][r].wumpus: tileString += "W"
        if self.__board[c][r].gold:   tileString += "G"
        if self.__board[c][r].breeze: tileString += "B"
        if self.__board[c][r].stench: tileString += "S"

        if self.__agentX == c and self.__agentY == r:
            if self.__agentDir == 0:
                tileString += ">"

            elif self.__agentDir == 1:
                tileString += "v"

            elif self.__agentDir == 2:
                tileString += "<"

            elif self.__agentDir == 3:
                tileString += "^"
          

        tileString += "."

        print(tileString.rjust(8), end="")

    def __printAgentInfo(self):
        
        print("AgentX: " + str(self.__agentX+1))
        print("AgentY: " + str(self.__agentY+1))
        self.__printPerceptInfo()


  
    def __printPerceptInfo(self):
        perceptString = "Percepts: "

        if self.__board[self.__agentX][self.__agentY].stench: perceptString += "Stench, "
        if self.__board[self.__agentX][self.__agentY].breeze: perceptString += "Breeze, "
        if self.__board[self.__agentX][self.__agentY].gold:   perceptString += "Glitter, "
        if self.__bump:                         perceptString += "Bump, "
        if self.__scream:                       perceptString += "Scream"

        if perceptString[-1] == ' ' and perceptString[-2] == ',':
            perceptString = perceptString[:-2]

        print(perceptString)


    def __randomInt(self, limit):
        return random.randrange(limit)
