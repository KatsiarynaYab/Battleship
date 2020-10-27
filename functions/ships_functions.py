import config

from functions import game_functions
from game_elements.game_errors import WrongShipsPosition
from game_elements.ship import Ship


def create_ships(ship_array):
    ship_array.append(Ship(4))
    for i in range(0, 2):
        ship_array.append(Ship(3))
    for i in range(0, 3):
        ship_array.append(Ship(2))
    for i in range(0, 4):
        ship_array.append(Ship(1))


def surround_ship(ship, field):
    for n in range(ship.cell_y - 1, ship.cell_y + ship.cell_height + 1):
        for m in range(ship.cell_x - 1, ship.cell_x + ship.cell_width + 1):
            if 0 <= n < config.cells_in_row_number:
                if 0 <= m < config.cells_in_row_number:
                    if field[n][m] not in (1, -1):
                        field[n][m] = 2


# TODO: class method

def add_ship_to_field(ship, i, j, field):
    ship.cell_x = j
    ship.cell_y = i
    for k in range(0, ship.size):
        field[i][j] = 1
        if ship.horizontal:
            j += 1
        else:
            i += 1


def draw_ships(screen, ship_array):
    for ship in ship_array:
        if ship.visible:
            ship.update(screen)


def count_ships(ship_array):
    count_arr = [0, 0, 0, 0]
    for ship in ship_array:
        if not ship.killed:
            count_arr[ship.size - 1] += 1
    return count_arr


def set_start_player_ships_position(player_ship_array):
    # Set start position to ships
    y = config.border_size + config.field_width + config.border_size
    coordinates = (config.border_size, y)
    switch_to_second_line = False
    for ship in player_ship_array:
        ship.set_default_coordinates(coordinates)
        coordinates = (coordinates[0] + config.border_size + config.cell_width * ship.size, coordinates[1])
        # switch to second line
        if coordinates[0] > 700 and not switch_to_second_line:
            coordinates = (config.border_size, y + config.border_size)
            switch_to_second_line = True


# define ship coordinates for field array
def add_ships_to_field(field, ship_array, field_x, field_y):
    for ship in ship_array:
        i, j = game_functions.xy_to_ij(ship.x - field_x, ship.y - field_y)
        if can_place_ship_here(field, i, j, ship):
            add_ship_to_field(ship, i, j, field)
        else:
            game_functions.clear_field(field)
            raise WrongShipsPosition(j, i)


def can_place_ship_here(field, i, j, ship):
    # check if ship
    # check if any other ship is in ship surrounding
    for n in range(i - 1, i + ship.cell_height + 1):
        for m in range(j - 1, j + ship.cell_width + 1):
            if game_functions.correct_coordinates(n, m):
                if field[n][m] == 1:
                    return False
    return True


def hide_ships(ship_array):
    for ship in ship_array:
        ship.hide()


def all_ships_on_player_field(ship_array):
    for ship in ship_array:
        if not ship.on_player_field():
            return False
    return True


def fix_ships(ships_array):
    for ship in ships_array:
        ship.fix_on_place()
