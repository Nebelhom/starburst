#!/usr/bin/python
from objects import *
from main import DIMENSIONS

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
WIDHT, HEIGHT = DIMENSIONS

# definitions of objects
small_starburst = {
    'class': Starburst,
    'colour': (255, 255, 255),
    'size': 5,
    'speed': 16,
    'exp_max_size': 20,
    'score': 100
}

reg_starburst = {
    'class': Starburst,
    'colour': (255, 255, 255),
    'size': 10,
    'speed': 15,
    'exp_max_size': 40,
    'score': 50
}

large_starburst = {
    'class': Starburst,
    'colour': (255, 255, 255),
    'size': 15,
    'speed': 13,
    'exp_max_size': 60,
    'score': 25
}



lvl_test0 = {'Game': {
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

lvl_test1 = {'Game': {
            'sim_time': 4.0
        },
        'MovingObjects': [
        {
            'angle': 0.5,
            'posx': 100,
            'type': reg_starburst,
            'toc': 1.0,
        },
        {
            'angle': -0.5,
            'posx': WIDHT-100,
            'type': small_starburst,
            'toc': 1.0,
        },
        {
            'angle': 0.0,
            'posx': WIDHT / 2,
            'type': large_starburst,
            'toc': 1.0,
        }
        ]
}