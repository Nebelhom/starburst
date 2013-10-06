#!/usr/bin/python
from objects import *
from constants import DIMENSIONS, WHITE, BLACK, BLUE, GREEN, RED, PURPLE

"""
Moving Objects
# Outside Factors - defined in main.py and settings.py
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
WIDTH, HEIGHT = DIMENSIONS

# definitions of objects
small_starburst = {
    'class': Starburst,
    'colour': WHITE,
    'exp_max_size': 20,
    'score': 100,
    'size': 5,
    'speed': 16
}

reg_starburst = {
    'class': Starburst,
    'colour': WHITE,
    'exp_max_size': 40,
    'score': 50,
    'size': 10,
    'speed': 15
}

large_starburst = {
    'class': Starburst,
    'colour': WHITE,
    'exp_max_size': 60,
    'score': 25,
    'size': 15,
    'speed': 13
}

double_score = {
    'class': DoubleScore,
    'colour': GREEN,
    'exp_max_size': 10,
    'score': None,
    'size': 10,
    'speed': 15
}

quadruple_score = {
    'class': QuadrupleScore,
    'colour': PURPLE,
    'exp_max_size': 5,
    'score': None,
    'size': 5,
    'speed': 15
}

half_score = {
    'class': HalfScore,
    'colour': RED,
    'exp_max_size': 10,
    'score': None,
    'size': 20,
    'speed': 15
}

#################
## Test Levels ##
#################

# Test if Starburst are correctly displayed
lvl_test0 = {'Game': {
    'sim_time': 4.0,
    'num_charges': 1,
},
    'MovingObjects': [
    {
        'angle': 0.0,
        'posx': 100,
        'type': reg_starburst,
        'toc': 1.0,
    },
    {
        'angle': 0.5,
        'posx': 300,
        'type': reg_starburst,
        'toc': 1.0,
    },
    {
        'angle': -0.25,
        'posx': 350,
        'type': reg_starburst,
        'toc': 1.0,
    },
    {
        'angle': 0.0,
        'posx': 110,
        'type': reg_starburst,
        'toc': 1.5,
    },
    {
        'angle': -0.33,
        'posx': 100,
        'type': reg_starburst,
        'toc': 2.0,
    },
    {
        'angle': 0.33,
        'posx': 400,
        'type': reg_starburst,
        'toc': 1.0
        }]
}

# Test if Collision Detection of Starbursts (and Explosions) work
lvl_test1 = {'Game': {
    'sim_time': 4.0,
    'num_charges': 1,
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
            'posx': WIDTH - 100,
            'type': small_starburst,
            'toc': 1.0,
        },
        {
            'angle': 0.0,
            'posx': WIDTH / 2,
            'type': large_starburst,
            'toc': 1.0,
        }
    ]
}

# Test if Explosions do not bounce on wall but just stick
lvl_test2 = {'Game': {
    'sim_time': 4.0,
    'num_charges': 1,
},
    'MovingObjects': [
        {
            'angle': -0.4,
            'posx': 300,
            'type': reg_starburst,
            'toc': 1.0,
        }]
}

# Test if half and doublescore works
lvl_test3 = {'Game': {
    'sim_time': 4.0,
    'num_charges': 1,
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
            'posx': WIDTH - 100,
            'type': small_starburst,
            'toc': 1.0,
        },
        {
            'angle': 0.0,
            'posx': WIDTH / 2,
            'type': large_starburst,
            'toc': 1.0,
        },
        {
            'angle': 0.25,
            'posx': 250,
            'type': double_score,
            'toc': 1.0,
        },
        {
            'angle': -0.25,
            'posx': 450,
            'type': half_score,
            'toc': 1.0,
        }
    ]
}

# Test if conversion posx works
# in width = 640 a quarter is 160
lvl_test4 = {'Game': {
    'sim_time': 4.0,
    'num_charges': 0,
},
    'MovingObjects': [
        {
            'angle': 0.0,
            'posx': 0.25,
            'type': reg_starburst,
            'toc': 1.0,
        }
    ]
}
