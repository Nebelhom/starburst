#!/usr/bin/env python

"""
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

# If ESC called in between actions need to clear all variables again before returning to menu

# implement game with explosions and score
# Give and endscreen how much the player scored

import sys
from datetime import datetime

import pygame
from pygame.locals import *

from levels import *
from settings import CONVERSIONS, DIFFICULTY, BLACK, BLUE, RED, WHITE

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
        self.charges = []
        self.cur_time = None  # defined in loop

    def clear_variables(self):
        # Game variables
        self.bursts = []
        self.explosions = []
        self.cur_time = None  # defined in loop

    def display_explanation(self):
        """
        Explains the game and returns 0 when pressing Esc
        and 1 when pressing Space.
        """
        while True:
            # Limit frame speed to 50 FPS
            time_passed = self.clock.tick(50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return 0
                    elif event.key == pygame.K_SPACE:
                        return 1

            # Redraw the background
            self.screen.fill(self.bg_color)

            # Create the text
            self.exp_font = pygame.font.SysFont('None', 30)

            expl1 = "Watch the simulation and then"
            expl2 = "place the charges in strategic positions."
            expl3 = "To place them do a left-click,"
            expl4 = "To remove them do a right-click."
            expl5 = "Detonate them in the game by pressing SPACE."
            expl6 = "Press <SPACE> to continue or"
            expl7 = "<ESC> to return to the start menu."

            expl1_text = self.exp_font.render(expl1, 0, WHITE)
            expl2_text = self.exp_font.render(expl2, 0, WHITE)
            expl3_text = self.exp_font.render(expl3, 0, WHITE)
            expl4_text = self.exp_font.render(expl4, 0, WHITE)
            expl5_text = self.exp_font.render(expl5, 0, WHITE)
            expl6_text = self.exp_font.render(expl6, 0, WHITE)
            expl7_text = self.exp_font.render(expl7, 0, WHITE)

            # Bring it to the screen
            self.screen.blit(expl1_text, (40, 100))
            self.screen.blit(expl2_text, (40, 120))
            self.screen.blit(expl3_text, (40, 140))
            self.screen.blit(expl4_text, (40, 160))
            self.screen.blit(expl5_text, (40, 180))
            self.screen.blit(expl6_text, (40, 220))
            self.screen.blit(expl7_text, (40, 240))

            pygame.display.flip()

    def display_score(self):
        """
        Displays the final score and returns 0 when pressing Esc
        and 1 when pressing Space.
        """
        while True:
            # Limit frame speed to 50 FPS
            time_passed = self.clock.tick(50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_SPACE:
                        sys.exit()

            # Redraw the background
            self.screen.fill(self.bg_color)

            # Create the text
            #self.exp_font = pygame.font.SysFont('None', 30)

            final_score = "Your final score is %d" % self.score
            instructions1 = "Press <ESC> to return to menu or"
            instructions2 = "<SPACE> to exit the game."

            fscore_text = self.exp_font.render(final_score, 0, WHITE)
            instr1_text = self.exp_font.render(instructions1, 0, WHITE)
            instr2_text = self.exp_font.render(instructions2, 0, WHITE)

            # Bring it to the screen
            self.screen.blit(fscore_text, (40, self.screen.get_height() / 2 - 60))
            self.screen.blit(instr1_text, (40, self.screen.get_height() / 2))
            self.screen.blit(instr2_text, (40, self.screen.get_height() / 2 + 20))

            pygame.display.flip()

    def draw_static_text(self):
        """Displays score and time countdown in top right corner"""

        # Create the text
        self.s_text = "Score: %d" % (self.score)
        self.score_text = self.font.render(self.s_text, 0, WHITE)
        self.t_text = "Time left: %.2f" % (self.time)
        self.time_text = self.font.render(self.t_text, 0, WHITE)
        self.c_text = "Charges left: %d" % (self.num_charges)
        self.charges_text = self.font.render(self.c_text, 0, WHITE)

        # Bring it to the screen
        self.screen.blit(self.score_text, (0, 0))
        height_diff = self.score_text.get_rect()[3]
        self.screen.blit(self.time_text, (0, height_diff))
        self.screen.blit(self.charges_text, (0, height_diff * 2))

    def draw_the_action(self, cur_time, time_passed):
        """Draws the moving parts of the simulation."""
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
                    self.increment_score(burst)
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

    def increment_score(self, burst):
        """
        Increment self.score.

        Moving object is part of the StarBurst class

        """
        self.score += burst.score

    def read_game_params(self, lvl_dict):
        # simulation time in seconds
        self.simulation_time = lvl_dict['Game']['sim_time']
        self.num_charges = lvl_dict['Game']['num_charges']

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
        start = datetime.now()

        self.read_lvl(lvl)
        self.time = self.simulation_time

        mainloop = True
        while mainloop:
            # Limit frame speed to 50 FPS
            time_passed = self.clock.tick(50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.clear_variables()
                        self.charges = []
                        return
                    if event.key == pygame.K_SPACE and \
                            self.num_charges == 0:
                        self.clear_variables()
                        return 1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.num_charges > 0:
                        mpos = pygame.mouse.get_pos()
                        detonator = Detonator(self.screen, mpos)
                        self.charges.append(detonator)
                        self.num_charges -= 1
                    if pygame.mouse.get_pressed()[2] == 1 and \
                            self.charges != []:
                        self.charges.pop()
                        self.num_charges += 1

            self.cur_time = (datetime.now() - start).total_seconds()
            # Adjust simulation time
            self.time = self.simulation_time - self.cur_time

            # Redraw the background
            self.screen.fill(self.bg_color)
            self.draw_static_text()

            for charge in self.charges:
                charge.display()
                if not charge.alive:
                    self.charges.remove(charge)

            self.draw_the_action(self.cur_time, time_passed)

            if self.num_charges == 0:
                # Create the text
                self.continue_font = pygame.font.SysFont('None', 30)
                cont = "If you are ready, press <SPACE> to start the game"
                cont_text = self.continue_font.render(cont, 0, BLUE)
                # Bring it to the screen
                halfway = self.screen.get_height() / 2
                self.screen.blit(cont_text, (40, halfway))

            pygame.display.flip()

            if self.cur_time > self.simulation_time and self.bursts == []:
                start = datetime.now()
                self.read_bursts(lvl)

                for burst in self.bursts:
                    burst.alive = True  # Revive them

    def run_game(self, lvl):
        start = datetime.now()

        self.read_lvl(lvl)
        self.time = self.simulation_time

        mainloop = True
        while mainloop:
            # Limit frame speed to 50 FPS
            time_passed = self.clock.tick(50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # empty all the values
                        self.clear_variables()
                        self.charges = []
                        return
                    if event.key == pygame.K_SPACE:
                        det = self.charges.pop(0)
                        # Stationary Explosion
                        new_exp = Explosion(det.explosion_size,
                                            self.screen,
                                            (det.x, det.y),
                                            angle=0,
                                            size=(det.width / 2),
                                            speed=0,
                                            scaling_factor=CONVERSIONS[self.width])
                        self.explosions.append(new_exp)

            self.cur_time = (datetime.now() - start).total_seconds()
            # Adjust simulation time
            if self.time > 0:
                self.time = self.simulation_time - self.cur_time

            # Redraw the background
            self.screen.fill(self.bg_color)
            self.draw_static_text()

            for charge in self.charges:
                charge.display()
                if not charge.alive:
                    self.charges.remove(charge)

            self.draw_the_action(self.cur_time, time_passed)

            pygame.display.flip()

            if self.cur_time > self.simulation_time and self.bursts == []:
                return 1

if __name__ == "__main__":
    # Creating the screen
    screen = pygame.display.set_mode((640, 480), 0, 32)

    pygame.display.set_caption('Game Menu')
    gm = Game(screen, BLACK)
    gm.run_simulation(lvl_test1)
