import sys
import pygame
from settings import Settings as game_settings

def check_events():
    pass

def xy_to_game_coordinates(x, y):
    return (game_settings.letters[y], game_settings.numbers[x])

def xy_to_ij(x, y):
    return (int(y/game_settings.cell_width), int(x/game_settings.cell_width))

def ij_to_xy(i, j):
    return j*game_settings.cell_width, i*game_settings.cell_width

def correct_coordinates(i, j):
    if i >= 0 and i < game_settings.cells_in_row_number:
        if j >= 0 and j < game_settings.cells_in_row_number:
            return True
    return False

def surround_ship(ship, field):
    for n in range(ship.cell_y-1, ship.cell_y + ship.cell_height+1):
        for m in range(ship.cell_x-1, ship.cell_x + ship.cell_width+1):
            if n >= 0 and n < game_settings.cells_in_row_number:
                if m >= 0 and m < game_settings.cells_in_row_number:
                    if field[n][m] not in (1, -1):
                        field[n][m] = 2


def shoot(ij_coordinates, field, ship_array):
    i, j = ij_coordinates
    if field[i][j] == 0:
        ##  missfire
        field[i][j] = 2
        return 'missfire'
    if field[i][j] == 1:
        for ship in ship_array:
            if ship.is_injured(i, j):
                ship.shoot(i, j)
                field[i][j] = -1
                if ship.is_killed():
                    surround_ship(ship, field)
                    return 'killed'
                return 'injured'
    if field[i][j] == -1:
        return 'already injured'
    if field[i][j] == 2:
        return 'already missfire'