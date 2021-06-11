import sys
import os
import math
from World import World
import turtle

def Rerun_Random_World():
    while True:
        print("---------------")
        response = input("Run another world? (y/n)\n")
        if response.lower() == "y" or response.lower() == "yes":
            turtle.reset()
            return True
        elif response.lower() == "n" or response.lower() == "no":
            return False
        else:
            print("Invalid Input: Response must be yes or no. (y/n)")
def main ( ):
    args = sys.argv
    while True:
        world = World(True)
        success= world.run()
        if success:
            print ("Success!!!")
        if not Rerun_Random_World():
            return

main()
