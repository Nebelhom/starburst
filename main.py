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
# Create an infinite simulation loop that repeats the same simulation again and again.(TICK)
# Consider reading in specific values from a dictionary for each "level" (Fine for now. Do so when the mechanics work)
# Create a mouseclick explosion (TICK)
# Create a collision detector. Collide with other Starburst and all is good, Collide with explosion and be converted
# -> maybe method for conversion...

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

class MovingObject:
    def __init__(self, screen, (x, y), speed, angle, scaling_factor):
        """
        screen: pygame surface instance
        (x, y): coordinates in pixels
        speed: in meters/second
        angle: in radians
        scaling_factor: Conversion factor from meters to pixels for speed
        """

        # Outside Factors
        self.screen = screen
        self.scaling = scaling_factor

        # Object intrinsic attributes
        self.x, self.y = x, y
        self.size = 10
        self.color = (255, 255, 255)
        self.speed = speed
        # self.angle in radians from 0 to math.pi*2
        self.angle = angle
        self.alive = True

    def display(self):
        if self.alive:
            pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.size)

    def move(self, time):
        """
        Calculates the new position, speed and direction of the Starburst

        time: time passed since last loop
        start_time: time at which simulation starts
        """
        if self.alive:
            time /= 1000.0
            self.angle, self.speed = addVectors((self.angle, self.speed), (GRAVITY_DIR, GRAVITY_STR * time))
            self.x += math.sin(self.angle) * self.speed * time * self.scaling
            self.y -= math.cos(self.angle) * self.speed * time * self.scaling

            # Below floor = kill it
            if self.y > self.screen.get_width() + self.size:
                self.alive = False

    def bounce(self):
        """
        Lets the Starburst bounce from the side walls.
        """
        width = self.screen.get_width()
        if self.x > width - self.size:
            self.x = 2 * (width - self.size) - self.x
            self.angle = -self.angle
        elif self.x < self.size:
            self.x = 2 * self.size - self.x
            self.angle = -self.angle

class Starburst(MovingObject):
    """
    The Starburst class that gets fired into the air and can
    explode.
    """
    def __init__(self, time_of_creation, *args, **kwargs):
        """
        time_of_creation: Gives time when it should start, in seconds
        """
        MovingObject.__init__(self, *args, **kwargs)

        self.toc = time_of_creation

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

class Explosion(MovingObject):
    def __init__(self, max_size=20, *args, **kwargs):

        MovingObject.__init__(self, *args, **kwargs)

        self.color = 255, 0, 0
        self.size = 1
        self.max_size = max_size

    def display(self):
        if self.alive:
            pygame.draw.circle(self.screen, self.color, (int(self.x), int(self.y)), self.size, 1)

    def explode(self):
        if self.size > self.max_size:
            self.alive = False
        else:
            self.size += 2


class Game:
    def __init__(self, dimensions=(640, 480), bg_color=(0, 0, 0),
                 simulation_time=10.0, caption="Starburst"):

        self.dimensions = self.width, self.height = dimensions
        self.bg_color = bg_color
        self.caption = caption

        # Creating the screen
        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
        pygame.display.set_caption(self.caption)
        self.clock = pygame.time.Clock()

        # simulation time in seconds
        self.simulation_time = simulation_time

    def create_bursts(self, num_bursts):
        bursts = []
        for i in range(num_bursts):
            burst = Starburst(uniform(0.0, self.simulation_time - 5),
                              self.screen,(randint(20, self.width - 20),
                                           self.height + 20),15,
                              uniform(-math.pi/4, math.pi/4),
                              CONVERSIONS[self.width])
            bursts.append(burst)
        return bursts

    def main(self):
        start = datetime.now()

        bursts = self.create_bursts(3)
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
                    exp = Explosion(40, self.screen,(mouseX, mouseY), 15,
                                    uniform(-math.pi/4, math.pi/4),
                                    CONVERSIONS[self.width])
                    explosions.append(exp)

            # Redraw the background
            self.screen.fill(self.bg_color)

            cur_time = (datetime.now() - start).total_seconds()

            for burst in bursts:
                # Update and redraw all circles
                burst.move(time_passed, cur_time)
                burst.bounce()
                burst.display()
                #print bursts
                if not burst.alive:
                    bursts.remove(burst) # No more calculations

            for exp in explosions:
                exp.explode()
                exp.display()
                if not exp.alive:
                    explosions.remove(exp)

            pygame.display.flip()

            if cur_time > self.simulation_time:
                # Should restart the simulation
                start = datetime.now()
                bursts = self.create_bursts(3)

######################
## Global Functions ##
######################

def addVectors((angle1, length1), (angle2, length2)):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2

    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return (angle, length)

if __name__ == '__main__':
    game = Game()
    game.main()