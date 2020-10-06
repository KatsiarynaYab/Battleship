import sys
import pygame
from settings import Settings as game_settings

def check_events():
    pass

def xy_to_game_coordinates(x, y):
    return (game_settings.letters[y], game_settings.numbers[x])

def xy_to_ji(x, y):
    return int(x/game_settings.cell_width), int(y/game_settings.cell_width)

def ij_to_xy(i, j):
    return j*game_settings.cell_width, i*game_settings.cell_width