import random

import config
import ships_functions


def check_events():
    pass


def ij_to_game_coordinates(i, j):
    return config.letters[j], config.numbers[i]


def xy_to_ij(x, y):
    return int(y / config.cell_width), int(x / config.cell_width)


def ij_to_xy(i, j):
    return j * config.cell_width, i * config.cell_width


def correct_coordinates(i, j):
    if 0 <= i < config.cells_in_row_number:
        if 0 <= j < config.cells_in_row_number:
            return True
    return False


def create_field(field):
    for i in range(0, config.cells_in_row_number):
        field.append([])
        for j in range(0, config.cells_in_row_number):
            field[i].append(0)


def clear_field(field):
    for i in range(0, len(field)):
        for j in range(0, len(field[i])):
            field[i][j] = 0


def shoot(ij_coordinates, field, ship_array):
    i, j = ij_coordinates
    if field[i][j] == 0:
        field[i][j] = 2     # missfire
        return 'missfire'
    if field[i][j] == 1:
        for ship in ship_array:
            if ship.injured(i, j):
                ship.shoot(i, j)
                field[i][j] = -1    # hited
                if ship.killed:
                    ships_functions.surround_ship(ship, field)
                    return 'killed'
                return 'hit'
    if field[i][j] == -1:
        return 'already hit'
    if field[i][j] == 2:
        return 'already missfire'


def randomize_field(field, ship_array, field_x, field_y):
    for ship in ship_array:
        i = random.randint(0, config.cells_in_row_number - 1)
        j = random.randint(0, config.cells_in_row_number - 1)
        horizontal = random.choice([True, False])
        if not horizontal:
            ship.change_angle()
        while not (i + ship.cell_height - 1 < config.cells_in_row_number
                   and j + ship.cell_width - 1 < config.cells_in_row_number) \
                or not ships_functions.can_place_ship_here(field, i, j, ship):
            i = random.randint(0, config.cells_in_row_number - 1)
            j = random.randint(0, config.cells_in_row_number - 1)
        # ship.fix_on_place()
        ship.update_coordinates((field_x + j * config.cell_width,
                                 field_y + i * config.cell_width))
        ships_functions.add_ship_to_field(ship, i, j, field)
    clear_field(field)


def click_on_enemy_field(pos):
    x, y = pos
    if config.enemy_field_x <= x <= config.enemy_field_x + config.field_width and \
            config.enemy_field_y <= y <= config.enemy_field_y + config.field_width:
        return True
    return False


def win(enemy_ship_array):
    for ship in enemy_ship_array:
        if not ship.killed:
            return False
    return True


def loose(player_ship_array):
    for ship in player_ship_array:
        if not ship.killed:
            return False
    return True
