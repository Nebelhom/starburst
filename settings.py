#!/usr/bin/env python

import math

DIMENSIONS = (640, 480)

#GRAVITY = 10  # m per s
GRAVITY = GRAVITY_DIR, GRAVITY_STR = (math.pi, 10)

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# key: value = width: px/m
# used as scaling factor
CONVERSIONS = {
    640: 50,
    800: 62.5,
    1024: 80,
    1280: 100
}

DIFFICULTY = {
    'easy': 0.25,
    'medium': 0.5,
    'hard': 0.75,
    'nightmare': 1.0
}
