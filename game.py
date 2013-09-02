#!/usr/bin/env python

"""
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
# Implement difficulty levels by giving fractions of real gravity and speed to make it all slower...
# (*0.25, 0.5, 0.75 and 1.0)

import pygame

from datetime import datetime
from pygame.locals import *

from levels import *
from settings import CONVERSIONS, DIFFICULTY, BLACK, RED, WHITE

pygame.init()

# Give reference pixel amount and then convert
# e.g in 640x480 1m = 100px; in 1024x800 1m = 200px and then work from there

# Therefore create a conversion factor specific for each resolution
# and give all other vectors and magnitudes in meters

# see settings.py

class Game(object):
    def __init__(self, screen, bg_color, font="None", font_size=20, font_color=WHITE):

        self.screen = screen
        self.posx, self.posy, self.width, self.height = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.bg_color = bg_color
        # "Below Screen", of course! What did you think it meant?
        self.bs = self.height + 20

        self.score = 0
        # time is defined on loading level
        self.time = 0
        # defined on loading level using dict.get(key, None)
        self.num_charges = None

        # text font
        self.font_color = font_color
        self.font = pygame.font.SysFont(font, font_size)

        # Game variables
        self.bursts = []
        self.explosions = []
        self.cur_time = None # defined in loop

    def display_explanation(self):
        pass

    def draw_static_text(self):
        """Displays score and time countdown in top right corner"""

        # Create the text
        self.s_text = "Score: %d" % (self.score)
        self.score_text = self.font.render(self.s_text, 0, (255, 255, 255))
        self.t_text = "Time left: %.2f" % (self.time)
        self.time_text = self.font.render(self.t_text, 0, (255, 255, 255))

        # Bring it to the screen
        self.screen.blit(self.score_text, (0, 0))
        height_diff = self.score_text.get_rect()[3]
        self.screen.blit(self.time_text, (0, height_diff))

    def draw_the_action(self, cur_time, time_passed):
        # Redraw the background
        self.screen.fill(self.bg_color)
        self.draw_static_text()

        for i, burst in enumerate(self.bursts):
            # Update and redraw all circles
            burst.move(time_passed, cur_time)
            burst.bounce()
            # Collision detection
            for burst2 in self.bursts[i + 1:]:
                burst.collide(burst2)
            burst.display()
            if not burst.alive:
                self.bursts.remove(burst)  # No more calculations

        for exp in self.explosions:
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
                    self.explosions.append(new_exp)
                    self.bursts.remove(burst)
            exp.display()
            if not exp.alive:
                self.explosions.remove(exp)

        pygame.display.flip()

    def read_game_params(self, lvl_dict):
        # simulation time in seconds
        self.simulation_time = lvl_dict['Game']['sim_time']

    def read_bursts(self, lvl_dict):
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
        self.score_text = self.font.render("Score: %d" % (self.score), 0,
                                           self.font_color)
        start = datetime.now()

        self.read_lvl(lvl)
        self.time = self.simulation_time

        mainloop = True
        while mainloop:
            # Limit frame speed to 50 FPS
            time_passed = self.clock.tick(50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mainloop = False

            self.cur_time = (datetime.now() - start).total_seconds()
            # Adjust simulation time
            self.time = self.simulation_time - self.cur_time
            self.draw_the_action(self.cur_time, time_passed)

            if self.cur_time > self.simulation_time and self.bursts == []:
                start = datetime.now()
                self.read_bursts(lvl)

                for burst in self.bursts:
                    burst.alive = True  # Revive them

        # Once out let real game be called from Main. Only return certain values like coordinates etc.

if __name__ == "__main__":
    # Creating the screen
    screen = pygame.display.set_mode((640, 480), 0, 32)

    pygame.display.set_caption('Game Menu')
    gm = Game(screen, BLACK)
    gm.run_simulation(lvl_test1)