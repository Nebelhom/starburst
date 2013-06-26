#!/usr/bin/env python

"""
Several objects are fired into the air at random times and fall down to earth.

At a time of the players chosing, he can press a button whenever and wherever he likes.
This will create an explosion (a radius). Every object that touches it, will also explode
(different radius for different objects).

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
"""

# TODO:
# Kill the Starburst when it is below the floor (TICK)
# Create an infinite simulation loop that repeats the same simulation again and again.
# Consider reading in specific values from a dictionary for each "level"

import math
import pygame

from datetime import datetime
from pygame.locals import *
from random import random, randint, uniform

pygame.init()

# Give reference pixel amount and then convert
# e.g in 640x480 1m = 100px; in 1024x800 1m = 200px and then work from there

# Therefore create a conversion factor specific for each resolution
# and give all other vectors and magnitudes in meters


#GRAVITY = 10  # m per s
GRAVITY = GRAVITY_DIR, GRAVITY_STR = (math.pi, 10)

# key: value = width: px/m
# used as scaling factor
CONVERSIONS = {
    640: 50,
    800: 62.5,
    1024: 80,
    1280: 100
}

def addVectors((angle1, length1), (angle2, length2)):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2

    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return (angle, length)

class BasicStarburst:
    """
    The basic Starburst class that gets fired into the air and can
    explode.
    """
    def __init__(self, screen, (x, y), speed, angle, scaling_factor,
                 time_of_creation):
        """
        screen: pygame surface instance
        (x, y): coordinates in pixels
        speed: in meters/second
        angle: in radians
        scaling_factor: Conversion factor from meters to pixels for speed
        time_of_creation: Gives time when it should start, in seconds
        """

        # Outside Factors
        self.screen = screen
        self.scaling = scaling_factor
        self.toc = time_of_creation

        # Object intrinsic attributes
        self.x, self.y = x, y
        self.size = 10
        self.colour = (255, 255, 255)
        self.speed = speed
        # self.angle in radians from 0 to math.pi*2
        self.angle = angle
        self.alive = True

    def display(self):
        if self.alive:
            pygame.draw.circle(self.screen, self.colour, (int(self.x), int(self.y)), self.size)

    def move(self, time, cur_time):
        """
        Calculates the new position, speed and direction of the Starburst

        time: time passed since last loop
        start_time: time at which simulation starts
        """
        if cur_time >= self.toc and self.alive:
            time /= 1000.0
            self.angle, self.speed = addVectors((self.angle, self.speed), (GRAVITY_DIR, GRAVITY_STR * time))
            self.x += math.sin(self.angle) * self.speed * time * self.scaling
            self.y -= math.cos(self.angle) * self.speed * time * self.scaling

            # Below floor = kill it
            if self.y > self.screen.get_width() + self.size:
                self.alive = False

    def bounce(self):
        """
        Lets the BasicStarburst bounce from the side walls.
        """
        width = self.screen.get_width()
        if self.x > width - self.size:
            self.x = 2 * (width - self.size) - self.x
            self.angle = -self.angle
        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = -self.angle


def main():
    start = datetime.now()
    # simulation time in seconds
    simulation_time = 25.0

    DIMENSION = WIDTH, HEIGHT = 640, 480
    BG_COLOUR = 0, 0, 0

    # Creating the screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    pygame.display.set_caption('Starburst')
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()

    num_bursts = 1
    bursts = []
    for i in range(num_bursts):
        burst = BasicStarburst(screen,
                               (randint(20, WIDTH - 20), HEIGHT),
                               15,
                               uniform(-math.pi/4, math.pi/4),
                               CONVERSIONS[WIDTH],
                               uniform(0.0, simulation_time - 5))
        bursts.append(burst)

    mainloop = True
    while mainloop:
        # Limit frame speed to 50 FPS
        time_passed = clock.tick(50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False

        # Redraw the background
        screen.fill(BG_COLOUR)

        cur_time = (datetime.now() - start).total_seconds()

        for burst in bursts:
            # Update and redraw all circles
            burst.move(time_passed, cur_time)
            burst.bounce()
            burst.display()
            print burst.y
            if not burst.alive:
                bursts.remove(burst) # No more calculations

        pygame.display.flip()

if __name__ == '__main__':
    main()