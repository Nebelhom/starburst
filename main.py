#!/usr/bin/env python

"""
Several objects are fired into the air at random times and fall down to earth.

Game Mechanics Possibilty 2 (Tendency goes to this one. Seems simpler...)
The player sees a simulation of what is happening and can then decide where to
place a certain amount of charges and decides on clicking, when to detonate them.

From the first explosion, it will be counted how many other objects have been exploded
incrementing the score.

Ideally, free style with random stuff mode and afterwards some kinda levels.

Different types of Starbursts

three different sizes for three different explosion radii (the smaller one get more points)

Special Starburst:
    - No explosion and extra points
    - Freeze movement for 2 seconds
    - Slow motion movement for 5 seconds
    - Speed up explosion
    - Score deductions

Number of explosions available could vary, too...

Brainstorming on saving level information. What needs to be in there?

    - a list of all the moving objects and their respective details
    - level information such as if there is a blockade in the way or not
"""

# TODO:
# Kill the Starburst when it is below the floor (TICK)
# Create an infinite simulation loop that repeats the same simulation again and again.(TICK)
# Consider reading in specific values from a dictionary for each "level" (Fine for now. Do so when the mechanics work)
# Create a mouseclick explosion (TICK)
# Create a collision detector. Collide with other Starburst and all is good, Collide with explosion and be converted
# -> maybe method for conversion...
# Implement difficulty levels by giving fractions of real gravity and speed to make it all slower...
# (*0.25, 0.5, 0.75 and 1.0)

import sys

import pygame

from _functools import partial
from pygame.locals import *

from game import Game
from gameMenu import GameMenu
from levels import *
from settings import DIFFICULTY, DIMENSIONS, BLACK, RED, WHITE

pygame.init()


class Main(object):
    def __init__(self, dimensions=DIMENSIONS, bg_color=BLACK,
                 caption="Starburst"):
        
        self.dimensions = self.width, self.height = dimensions
        self.bg_color = bg_color
        self.caption = caption

        # Creating the screen
        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
        pygame.display.set_caption(self.caption)
        self.clock = pygame.time.Clock()

    def empty_func(self):
        print "Empty!"

    def main(self):
        # Object initialisation

        # Main Game
        self.game = Game(self.screen, self.bg_color)

        # Game Menu
        menu_items = ('Start', 'Help', 'Quit')
        funcs = {
            'Start': partial(self.game.run_simulation, lvl_test1),
            'Help': self.empty_func,
            'Quit': sys.exit
        }
        self.gm = GameMenu(self.screen, menu_items, funcs, self.bg_color)

        # Start the show
        self.gm.run()

if __name__ == '__main__':
    game = Main()
    game.main()