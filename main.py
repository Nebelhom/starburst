#!/usr/bin/env python

# TODO:
# Implement difficulty levels by giving fractions of real gravity and speed to make it all slower...
# (*0.25, 0.5, 0.75 and 1.0)

import sys

import pygame
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

    def main(self):
        # Object initialisation

        # Main Game
        self.game = Game(self.screen, self.bg_color)

        # Game Menu
        menu_items = ('Play Highscore', 'Help', 'Quit')
        self.gm = GameMenu(self.screen, menu_items, self.bg_color)
        gatekeeper = None

        # Start the show
        while True:
            if gatekeeper:
                choice == "Play Highscore"
            else:
                choice = self.gm.run()
            if choice == 'Play Highscore':
                expl = self.game.display_explanation()
                if expl == 1:
                    sim = self.game.run_simulation(lvl_test1)
                    if not sim:
                        continue
                    game = self.game.run_game(lvl_test1)
                    if not game:
                        continue
                    gatekeeper = self.game.display_score()
                else:
                    pass
            elif choice == 'Help':
                pass
            else:
                sys.exit()

if __name__ == '__main__':
    game = Main()
    game.main()
