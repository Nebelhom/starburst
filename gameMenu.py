#!/usr/bin/python

import pygame
from pygame.constants import KEYDOWN, QUIT, K_ESCAPE, MOUSEMOTION
from pygame.locals import *

pygame.init()


"""
Create menu from screen input given in Main

Choices and effects are connected via functions in dict.

e.g. choices = {
                'Quit': sys.exit,
                'Start': Game().run
}

then if 'Quit': choices['Quit']()

elif 'Start': choices['Start']()

...at least see if that works
"""

class GameMenu():
    def __init__(self, screen, bg_color=(0,0,0), font='Arial', font_size=30, font_color=(255,255,255), menu_items=('Start', 'Settings', 'Quit')):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        self.bg_color = bg_color
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color

        self.items = []
        for item in menu_items:
            label = self.font.render(item, 1, font_color)
            width = label.get_rect().width
            height = label.get_rect().height
            self.items.append([label, width, height])

        self.sum_item_height = len(menu_items) * self.items[0][2]

    def insert_menu_items(self):
        for index, item in enumerate(self.items):
            label, width, height = item
            posx = (self.scr_width/2) - (width/2)
            posy = (self.scr_height/2) - (self.sum_item_height/2 + (index * height))
            self.screen.blit(label,(posx, posy))


    def run(self):
        """Creates the mainloop of the simulation"""
        mainloop = True
        while mainloop:
            # Limit frame speed to 50 FPS
            time_passed = self.clock.tick(50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = pygame.mouse.get_pos()

            # Redraw the background
            self.screen.fill(self.bg_color)

            self.insert_menu_items()

            pygame.display.flip()


class Main(object):
    def __init__(self, dimensions=(640, 480), bg_color=(0, 0, 0),
                 caption="Game Menu"):

        self.dimensions = self.width, self.height = dimensions
        self.bg_color = bg_color
        self.caption = caption

        # Creating the screen
        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
        pygame.display.set_caption(self.caption)
        self.clock = pygame.time.Clock()

    def main(self):
        # Creating the menu
        #self.menu = GameMenu()
        #self.menu.run()
        pass

        # Once the Menu is done, run the game...

if __name__ == "__main__":
    #main = Main()
    #main.main()

    # Creating the screen
    screen = pygame.display.set_mode((640, 480), 0, 32)
    pygame.display.set_caption('Game Menu')

    bg_color = (0,0,0)

    gm = GameMenu(screen, bg_color)
    gm.run()