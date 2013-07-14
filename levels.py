#!/usr/bin/python
from objects import *

"""
Moving Objects
# Outside Factors - defined in main.py
self.screen = screen
self.scaling = scaling_factor

----------------------------------
# Object intrinsic attributes

----------------------------------
Defined in separate dict for easiness
self.size = 10
self.color = (255, 255, 255)
self.speed = speed

----------------------------------

Need to be defined here
self.x, self.y = x, y
# self.angle in radians from 0 to math.pi*2
self.angle = angle

StarBurst
self.toc = time_of_creation
"""

# Note if posy not given, then it is a point just below the screen defined in
# Game() of main.py

# definitions of objects
reg_starburst = {
    'class': Starburst,
    'colour': (255, 255, 255),
    'size': 10,
    'speed': 15,
    'exp_max_size': 40
}

lvl0 = {'Game': {
            'sim_time': 4.0
        },
        'MovingObjects': [
        {
            'angle': 0.0,
            'posx': 100,
            'type': reg_starburst,
            'toc': 1.0,
        }]
}