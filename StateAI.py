
from tkinter.font import BOLD
from Agent import Agent
import turtle
screen = turtle.Screen()
screen.bgpic("grid.png")
screen.setup(600,550)
turtle.title('Wumpus World')



class StateAI(Agent):

    def __init__(self):
        turtle.penup()
        turtle.goto(-100, -100)
        turtle.shape('classic')
        self.__moves = 0
        self.__safe_tiles = []
        self.__tile_history = []
        self.__x_tile = 1
        self.__y_tile = 1
        self.__dir = 'E'
        self.__move_history = []
        self.__has_gold = False
        self.__revert_home = False
        self.__xBorder = 0
        self.__yBorder = 0

        self.__messageY = -150

        self.__dead_wump = False
        self.__found_wump = False

        self.__wump_node = (0, 0)
        self.__pit_node = (0, 0)
        self.__found_pit = False
        self.__stench_nodes = []
        self.__breeze_nodes = []
        self.__shot_arrow = False
        self.__backnode = (0, 0)
 
    def getXY(self, __x_tile, __y_tile) :
        XY = "(" + str(__x_tile)+","+str(__y_tile)+") "
        return turtle.write(XY, align="right")

    def setHome(self, __x_tile, __y_tile, pit , wumpus):
        if pit:
            turtle.goto(-60, self.__messageY)
            turtle.write("you die because of pit", font=("",11,BOLD))
            self.__messageY = self.__messageY -16
            turtle.goto(-100, -100)
            turtle.penup()
            if self.__dir == "N":
                turtle.setheading(90)
            elif self.__dir == "S":
                turtle.setheading(270)
            elif self.__dir == "w":
                turtle.setheading(180)
            self.__pit_node = (__x_tile, __y_tile)
            self.__found_pit = True

        if wumpus:
            turtle.goto(-60, self.__messageY)
            turtle.write("you die because of wumpus", font=("",11,BOLD))
            self.__messageY = self.__messageY -16
            turtle.goto(-100, -100)
            turtle.penup()
            if self.__dir == "N":
                turtle.setheading(90)
            elif self.__dir == "S":
                turtle.setheading(270)
            elif self.__dir == "W":
                turtle.setheading(180)
            self.__wump_node = (__x_tile, __y_tile)
            self.__found_wump = True

        (self.__x_tile, self.__y_tile) = (1, 1)

    def getPercept(self, stench, breeze, glitter, bump, scream, caution):
        turtle.color('white')
        turtle.write('■■■',font=("", 11))
        turtle.write('■■',font=("", 12))
        turtle.color('black')
        map_code = ""
        if caution == 1 :
            map_code = map_code + "P"
        if caution == 2 :
            map_code = map_code + "W"
        if caution == 3 :
            map_code = map_code + "PW"
        if bump:
            map_code = map_code + "WALL"
            return turtle.write(map_code,font=("", 11))


        if glitter:
            map_code = map_code + "G" 

        if breeze:
            map_code = map_code + "B"

        if stench:
            map_code = map_code + "S"

        return turtle.write(map_code,font=("", 11))
        
            

    def getAction(self, stench, breeze, glitter, bump, scream):

        self.__check_bump(bump)
        self.__update_history_tiles()

        self.__moves += 1
        return self.__deter(stench, breeze, glitter, bump, scream)


    class Node:
        def __init__(self, x, y):
            self.__node = (x, y)
            self.__Nnode = (x, y + 1)
            self.__Enode = (x + 1, y)
            self.__Snode = (x, y - 1)
            self.__Wnode = (x - 1, y)

        def getCurrent(self):
            return self.__node

        def getNorth(self):
            return self.__Nnode

        def getEast(self):
            return self.__Enode

        def getSouth(self):
            return self.__Snode

        def getWest(self):
            return self.__Wnode

        def getX(self):
            return self.__node[0]

        def getY(self):
            return self.__node[1]

  
    def __Facing_Wump(self):
        if self.__wump_node != (0,0):
            if self.__dir == "N":
                if self.__wump_node[1] > self.__y_tile:
                    return True
                else:
                    return False
            elif self.__dir == "E":
                if self.__wump_node[0] > self.__x_tile:
                    return True
                else:
                    return False
            elif self.__dir == "S":
                if self.__wump_node[1] < self.__y_tile:
                    return True
                else:
                    return False
            elif self.__dir == "W":
                if self.__wump_node[0] < self.__x_tile:
                    return True
                else:
                    return False
            return True
        return False

    def __deter(self, stench, breeze, glitter, bump, scream):

        # back to home
        if self.__revert_home:
            if self.__tile_history[len(self.__tile_history) - 1] == (self.__x_tile, self.__y_tile):
                self.__backnode = self.__tile_history.pop()

            while self.__backnode == (self.__x_tile, self.__y_tile):
                if self.__backnode == (1, 1):
                    return Agent.Action.CLIMB

                elif self.__x_tile - self.__tile_history[len(self.__tile_history) - 1][0] == 1:
                    return self.__GoWest()
                elif self.__x_tile - self.__tile_history[len(self.__tile_history) - 1][0] == -1:
                    return self.__GoEast()
                elif self.__y_tile - self.__tile_history[len(self.__tile_history) - 1][1] == 1:
                    return self.__GoSouth()
                else:
                    return self.__GoNorth()

        if glitter:
            self.__has_gold = True
            self.__revert_home = True
            current_x = turtle.xcor()
            current_y = turtle.ycor()
            
            turtle.goto(-60, self.__messageY)
            turtle.color('orange')
            turtle.write("You got gold", font=("",11,BOLD))
            turtle.shape('turtle')
            self.__messageY = self.__messageY -16
            turtle.goto(current_x,current_y)
            self.__move_history.append("GRAB")
            return Agent.Action.GRAB
        if stench:
            if self.__Facing_Wump():
                self.__shot_arrow = True
                current_x = turtle.xcor()
                current_y = turtle.ycor()
                turtle.shape('arrow')
                turtle.color('red')
                turtle.forward(70)
                turtle.goto(-60, self.__messageY)
                turtle.color('black')
                turtle.shape('classic')
                turtle.write("Shoot the Arrow!", font=("",11,BOLD))
                self.__messageY = self.__messageY -16
                turtle.goto(current_x,current_y)
                return Agent.Action.SHOOT
        if breeze:
            if self.__pit_node == (self.__x_tile + 1, self.__y_tile):
                return self.__GoNorth()
            elif self.__pit_node == (self.__x_tile, self.__y_tile + 1):
                return self.__GoWest()
            elif self.__pit_node == (self.__x_tile - 1, self.__y_tile):
                return self.__GoSouth()
            elif self.__pit_node == (self.__x_tile, self.__y_tile - 1):
                if self.__x_tile < self.__xBorder:
                    return self.__GoEast()
                else:
                    return self.__GoNorth()

        if scream:
            self.__dead_wump = True
            self.__found_wump = False
            if self.__wump_node not in self.__safe_tiles:
                self.__safe_tiles.append(self.__wump_node)
            self.__wump_node = (10, 10)


        # move
        if (self.__x_tile,self.__y_tile) == (3,2) and (4,2) in self.__tile_history:
            return self.__GoNorth()
        elif (self.__x_tile,self.__y_tile) == (3,3) and (4,3) in self.__tile_history:
            if (3,2) not in self.__tile_history:
                return self.__GoSouth()
            return self.__GoWest()
        elif (self.__x_tile, self.__y_tile) == (2,4) and (1,4) in self.__tile_history:
            return self.__GoSouth()
        elif (self.__x_tile, self.__y_tile) == (2,3) and (3,3) in self.__tile_history:
            if (1,3) not in self.__tile_history:
                return self.__GoWest()
            else: return self.__GoSouth()

            
        if (self.__x_tile, self.__y_tile) == (1, 1) and self.__has_gold:
            return Agent.Action.CLIMB
        elif self.__x_tile == self.__xBorder and self.__y_tile != self.__yBorder:
            return self.__GoNorth()
        elif self.__x_tile == 1 and self.__y_tile != self.__yBorder and (self.__x_tile, self.__y_tile) != (1, 1):
            if (self.__x_tile, self.__y_tile - 1) == (1, 1) and self.__has_gold:
                return self.__GoSouth()
            if (self.__x_tile, self.__y_tile - 1) not in self.__tile_history:
                return self.__GoSouth()
            else:
                return self.__GoEast()
        elif self.__x_tile == 1 and self.__y_tile == self.__yBorder:
            if (self.__x_tile + 1, self.__y_tile) in self.__tile_history:
                return self.__GoSouth()
            else:
                return self.__GoEast()
        elif self.__y_tile == self.__yBorder and self.__x_tile != self.__xBorder:

            return self.__GoWest()

        elif self.__x_tile == self.__xBorder and self.__y_tile == self.__yBorder:
            return self.__GoWest()
        else:
            return self.__GoEast()

 
    def __GoNorth(self):
        if self.__dir == 'N':  # N
            self.__move_history.append("FORWARD")
            self.__x_tile += self.__dir_to_coordinate(self.__dir)[0]
            self.__y_tile += self.__dir_to_coordinate(self.__dir)[1]
            turtle.forward(70)
            return Agent.Action.FORWARD
        elif self.__dir == 'E':  # E
            self.__dir = 'N'
            self.__move_history.append("LEFT")
            turtle.left(90)

            return Agent.Action.TURN_LEFT
        elif self.__dir == 'S':  # S
            self.__dir = 'E'
            self.__move_history.append("LEFT")
            turtle.left(90)

            return Agent.Action.TURN_LEFT
        elif self.__dir == 'W':  # W
            self.__dir = 'N'
            self.__move_history.append("RIGHT")
            turtle.right(90)

            return Agent.Action.TURN_RIGHT

    def __GoEast(self):
        if self.__dir == 'N':  # N
            self.__dir = 'E'
            self.__move_history.append("RIGHT")
            turtle.right(90)

            return Agent.Action.TURN_RIGHT
        elif self.__dir == 'E':  # E
            self.__move_history.append("FORWARD")
            self.__x_tile += self.__dir_to_coordinate(self.__dir)[0]
            self.__y_tile += self.__dir_to_coordinate(self.__dir)[1]
            turtle.forward(70)
            return Agent.Action.FORWARD
            
        elif self.__dir == 'S':  # S
            self.__dir = 'E'
            self.__move_history.append("LEFT")
            turtle.left(90)

            return Agent.Action.TURN_LEFT
        elif self.__dir == 'W':  # W
            self.__dir = 'S'
            self.__move_history.append("LEFT")
            turtle.left(90)

            return Agent.Action.TURN_LEFT

    def __GoSouth(self):
        if self.__dir == 'N':
            self.__dir = 'W'
            self.__move_history.append("LEFT")
            turtle.left(90)

            return Agent.Action.TURN_LEFT
        elif self.__dir == 'E':
            self.__dir = 'S'
            self.__move_history.append("RIGHT")
            turtle.right(90)

            return Agent.Action.TURN_RIGHT
        elif self.__dir == 'S':
            self.__move_history.append("FORWARD")
            self.__x_tile += self.__dir_to_coordinate(self.__dir)[0]
            self.__y_tile += self.__dir_to_coordinate(self.__dir)[1]
            turtle.forward(70)
            return Agent.Action.FORWARD
        elif self.__dir == 'W':
            self.__dir = 'S'
            self.__move_history.append("LEFT")
            turtle.left(90)

            return Agent.Action.TURN_LEFT

    def __GoWest(self):
        if self.__dir == 'N':
            self.__dir = 'W'
            self.__move_history.append("LEFT")
            turtle.left(90)

            return Agent.Action.TURN_LEFT
        elif self.__dir == 'E':
            self.__dir = 'N'
            self.__move_history.append("LEFT")
            turtle.left(90)

            return Agent.Action.TURN_LEFT
        elif self.__dir == 'S':
            self.__dir = 'W'
            self.__move_history.append("RIGHT")
            turtle.right(90)

            return Agent.Action.TURN_RIGHT
        elif self.__dir == 'W':
            self.__move_history.append("FORWARD")
            self.__x_tile += self.__dir_to_coordinate(self.__dir)[0]
            self.__y_tile += self.__dir_to_coordinate(self.__dir)[1]
            turtle.forward(70)
            return Agent.Action.FORWARD

    def __dir_to_coordinate(self, direction):
        if direction == 'N':
            return (0, 1)
        elif direction == 'E':
            return (1, 0)
        elif direction == 'S':
            return (0, -1)
        elif direction == 'W':
            return (-1, 0)
        else:
            return (0, 1)

    def __check_bump(self, bump):
        if (bump == True):
            turtle.backward(70)
            self.__x_tile -= self.__dir_to_coordinate(self.__dir)[0]
            self.__y_tile -= self.__dir_to_coordinate(self.__dir)[1]
            if self.__dir == 'N':
                self.__yBorder = self.__y_tile
            elif self.__dir == 'E':
                self.__xBorder = self.__x_tile

    def __update_history_tiles(self):
        if len(self.__tile_history) == 0:
            if (self.__x_tile, self.__y_tile) not in self.__tile_history:
                self.__tile_history.append((self.__x_tile, self.__y_tile))
        elif self.__tile_history[-1] != (self.__x_tile, self.__y_tile):
            if (self.__x_tile, self.__y_tile) not in self.__tile_history:
                self.__tile_history.append((self.__x_tile, self.__y_tile))
        if (self.__x_tile, self.__y_tile) not in self.__safe_tiles:
            self.__safe_tiles.append((self.__x_tile, self.__y_tile))

    def finish_ment(self):
        turtle.goto(-60, self.__messageY)
        turtle.color('red')
        turtle.write("Climb, You Win!", font=("",12,BOLD))
        self.__messageY = self.__messageY -16
        turtle.goto(-100,-100)


    turtle.listen()
