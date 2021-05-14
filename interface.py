from agent import Agent
from world import World


import time
from os import system
def wumpus_world():
    world = World()
    world.generate_world()
    time.sleep(1)
 
    agent = Agent(world)


    while agent.exited == False:
        agent.start()
        if agent.found_gold == True:
            
            print("You found the gold! VICTORY !")

        break


def main():

    wumpus_world()


main()
