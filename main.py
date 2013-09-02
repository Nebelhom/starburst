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

from datetime import datetime
from _functools import partial
from pygame.locals import *

from gameMenu import GameMenu
from levels import *

pygame.init()

# Give reference pixel amount and then convert
# e.g in 640x480 1m = 100px; in 1024x800 1m = 200px and then work from there

# Therefore create a conversion factor specific for each resolution
# and give all other vectors and magnitudes in meters

# This will be adjusted later to automatically recognise certain resolutions
DIMENSIONS = (640, 480)

# key: value = width: px/m
# used as scaling factor
CONVERSIONS = {
    640: 50,
    800: 62.5,
    1024: 80,
    1280: 100
}

# This is a factor 
DIFFICULTY = {
    'easy': 0.25,
    'medium': 0.5,
    'hard': 0.75,
    'nightmare': 1.0
}

class Main(object):
    def __init__(self, dimensions=DIMENSIONS, bg_color=(0, 0, 0),
                 caption="Starburst"):
        
        self.dimensions = self.width, self.height = dimensions
        self.bg_color = bg_color
        self.caption = caption

        # Creating the screen
        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
        pygame.display.set_caption(self.caption)
        self.clock = pygame.time.Clock()

        self.bs = self.height + 20
        # "Below Screen", of course! What did you think it meant?

    def read_game_params(self, lvl_dict):
        # simulation time in seconds
        self.simulation_time = lvl_dict['Game']['sim_time']

    def read_bursts(self, lvl_dict):
        self.bursts = []
        for mo in lvl_dict['MovingObjects']:
            mobj = mo['type']['class'](
                mo['type']['colour'],
                mo['type']['exp_max_size'],
                mo['type']['score'],
                mo['toc'],
                self.screen,
                (mo['posx'], self.bs),
                mo['angle'],
                mo['type']['size'],
                mo['type']['speed'],
                CONVERSIONS[self.width]
            )
            self.bursts.append(mobj)

    def read_lvl(self, lvl_dict):
        self.read_game_params(lvl_dict)
        self.read_bursts(lvl_dict)

    def run_simulation(self, lvl):
        start = datetime.now()

        self.read_lvl(lvl)
        explosions = []

        mainloop = True
        while mainloop:
            # Limit frame speed to 50 FPS
            time_passed = self.clock.tick(50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    # self.add_explosive(mouseX, mouseY)
                    exp = Explosion(
                        reg_starburst['exp_max_size'],
                        self.screen,
                        (mouseX, mouseY),
                        0.0,  # angle
                        1,    # size
                        0,    # speed
                        CONVERSIONS[self.width]
                    )
                    explosions.append(exp)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mainloop = False

            # Redraw the background
            self.screen.fill(self.bg_color)

            cur_time = (datetime.now() - start).total_seconds()

            for i, burst in enumerate(self.bursts):
                # Update and redraw all circles
                burst.move(time_passed, cur_time)
                burst.bounce()
                # Collision detection
                for burst2 in self.bursts[i+1:]:
                    burst.collide(burst2)
                burst.display()
                if not burst.alive:
                    self.bursts.remove(burst)  # No more calculations

            for exp in explosions:
                exp.explode()
                exp.move(time_passed)
                exp.bounce()
                # Collision detection
                for burst in self.bursts:
                    contact = exp.collide(burst)
                    # Checks for contact and converts burst to explosion
                    if contact:
                        new_exp = Explosion(
                            burst.exp_max_size,
                            self.screen,
                            (burst.x, burst.y),
                            burst.angle,
                            burst.size,
                            burst.speed,
                            CONVERSIONS[self.width]
                        )
                        explosions.append(new_exp)
                        self.bursts.remove(burst)
                exp.display()
                if not exp.alive:
                    explosions.remove(exp)

            pygame.display.flip()

            if cur_time > self.simulation_time and self.bursts == []:
                start = datetime.now()
                self.read_bursts(lvl)

                for burst in self.bursts:
                    burst.alive = True  # Revive them
    
    def run_startmenu(self):
        pass

    def main(self):
        menu_items = ('Start', 'Quit')
        funcs = {
            'Start': partial(self.run_simulation, lvl_test1),
            'Quit': sys.exit
        }
        self.gm = GameMenu(self.screen, menu_items, funcs, self.bg_color)
        self.gm.run()

if __name__ == '__main__':
    game = Main()
    game.main()