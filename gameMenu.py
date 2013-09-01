#!/usr/bin/python

import sys
import pygame

pygame.init()


class GameMenu():
    def __init__(self, screen, menu_items, funcs, bg_color=(0,0,0), font=None,
                 font_size=30, font_color=(255,255,255)):

        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height

        self.bg_color = bg_color
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(font, font_size)
        self.font_color = font_color

        self.items = []
        for index, item in enumerate(menu_items):
            label = self.font.render(item, 1, font_color)
            width = label.get_rect().width
            height = label.get_rect().height
            posx = (self.scr_width / 2) - (width / 2)
            t_h = len(menu_items) * height # t_h total_height
            posy = (self.scr_height / 2) - (t_h / 2) + (index * height)
            self.items.append([label, (width, height), (posx, posy), item])

        self.funcs = funcs

    def insert_menu_items(self):
        for label, dimensions, (posx, posy), name in self.items:
            self.screen.blit(label, (posx, posy))

    def is_selection(self, posx, posy, item):
        """
        Takes an item and checks if the coordinates of item coincide

        posx - integer value
        posy - integer value
        item - list of label, (width, height), (posx, posy)
        where:
            label  - pygame.font class
            width  - integer
            height - integer
            posx   - integer
            posy   - integer
        """
        if (posx >= item[2][0] and posx <= item[2][0] + item[1][0]) and \
                    (posy >= item[2][1] and posy <= item[2][1] + item[1][1]):
                return True
        return False

    def mark_selection(self, topleft, dimensions):
        """Draws a rectangle around the selected text"""
        self.select = pygame.draw.rect(self.screen, (255, 255, 255),
                                       pygame.Rect(topleft, dimensions), 1)

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
                    mx, my = pygame.mouse.get_pos()
                    for item in self.items:
                        if self.is_selection(mx, my, item):
                            self.funcs[item[-1]]()

            # Redraw the background
            self.screen.fill(self.bg_color)

            # Find mouse pos and mark selection if any
            mx, my = pygame.mouse.get_pos()
            for item in self.items:
                if self.is_selection(mx, my, item):
                    self.mark_selection(item[2], item[1])


            # Redraws the menu items
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

    gm = GameMenu(screen, ('Start', 'Quit'), bg_color, font='Ubuntu')
    gm.run()