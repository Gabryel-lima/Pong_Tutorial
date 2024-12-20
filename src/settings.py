import pygame
from os.path import join

WINDOW_WIDTH, WINDOW_HEIGHT = (700, 540) 
SIZE = {'paddle': (10, 100), 'ball': (15, 15)}
POS_BALL = {'ball': (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)}
POS = {'player': (WINDOW_WIDTH - 50, WINDOW_HEIGHT / 2), 'opponent': (50, WINDOW_HEIGHT / 2)}
SPEED = {'player': 500, 'opponent': 250, 'ball': 170}
COLORS = {
    'paddle': '#ee322c',
    'paddle shadow': '#b12521',
    'ball': '#ee622c',
    'ball shadow': '#c14f24',
    'bg': '#002633'
}

__all__ = [
    'pygame',
    'join',
    'WINDOW_WIDTH',
    'WINDOW_HEIGHT',
    'POS_BALL',
    'SIZE',
    'POS',
    'SPEED',
    'COLORS'
]
