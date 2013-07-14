#!/usr/bin/env python
import math
import pygame

pygame.init()

# Give reference pixel amount and then convert
# e.g in 640x480 1m = 100px; in 1024x800 1m = 200px and then work from there

# Therefore create a conversion factor specific for each resolution
# and give all other vectors and magnitudes in meters

#GRAVITY = 10  # m per s
GRAVITY = GRAVITY_DIR, GRAVITY_STR = (math.pi, 10)

class MovingObject:
    def __init__(self, screen, (x, y), angle, size, speed, scaling_factor):
        """
        screen: pygame surface instance
        (x, y): coordinates in pixels
        angle: in radians
        size: in pixels
        speed: in meters/second
        scaling_factor: Conversion factor from meters to pixels for speed
        """

        # Outside Factors
        self.scaling = scaling_factor
        self.screen = screen

        # Object intrinsic attributes
        self.alive = True
        self.angle = angle
        self.colour = (255, 255, 255)
        self.size = size
        self.speed = speed
        # self.angle in radians from 0 to math.pi*2
        self.x, self.y = x, y

    def display(self):
        if self.alive:
            pygame.draw.circle(self.screen, self.colour, (int(self.x), int(self.y)), self.size)

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
    There should be three different types: small, regular, large;
    They will vary in size, speed and explosion radius
    """
    def __init__(self, colour, time_of_creation, *args, **kwargs):
        """
        time_of_creation: Gives time when it should start, in seconds
        """
        MovingObject.__init__(self, *args, **kwargs)

        self.colour = colour
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
            self.size += 3

######################
## Global Functions ##
######################

def addVectors((angle1, length1), (angle2, length2)):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2

    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return (angle, length)