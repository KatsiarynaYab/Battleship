import sys
import pygame
import random
import time

import functions

from settings import Settings as game_settings
from game_errors import WrongShipsPosition
from field import Field
from help_window import HelpWindow
from ship import Ship
from button import Button

DOUBLECLICKTIME = 500

player_ship_array = []
enemy_ship_array = []
player_field = []
enemy_field = []
fire_array = []
missfire_array = []

def create_ships(ship_array):
    ship_array.append(Ship(4))
    for i in range(0, 2):
        ship_array.append(Ship(3))
    for i in range(0, 3):
        ship_array.append(Ship(2))
    for i in range(0, 4):
        ship_array.append(Ship(1))

def create_field(field):
    for i in range(0, game_settings.cells_in_row_number):
        field.append([])
        for j in range(0, game_settings.cells_in_row_number):
            field[i].append(0)

def clear_field(field):
    for list in field:
        for i in range(0, len(list)):
            list[i] = 0

def check_player_field():
    for list in player_field:
        for elem in list:
            if elem not in (0, 1, -1):
                return False
    return True


##for debugging
def show_field(field):
    for i in field:
        for j in i:
            print(j, end = ' ')
        print('\n')
    print('\n')

def start_game():
    pass


def set_start_ships_position():
    #Set start position to ships
    y = game_settings.border_size + game_settings.field_width + game_settings.border_size
    coordinates = (game_settings.border_size, y)
    switch_to_second_line = False
    for ship in player_ship_array:
        ship.set_default_coordinates(coordinates)
        coordinates = (coordinates[0] + game_settings.border_size + game_settings.cell_width*ship.size, coordinates[1])
        #switch to second line
        if coordinates[0] > 700 and switch_to_second_line == False:
            coordinates = (game_settings.border_size, y + game_settings.border_size)
            switch_to_second_line = True


def draw_ships(screen, ship_array):
    for ship in ship_array:
        if ship.is_visible():
            ship.update(screen)


def ship_on_the_field(ship):
    optimizer = game_settings.cell_width/2
    if ship.x + optimizer > game_settings.border_size and ship.y + optimizer > game_settings.border_size \
            and ship.x + ship.ship_body_width - optimizer < game_settings.border_size + game_settings.field_width \
            and ship.y + ship.ship_body_height - optimizer < game_settings.border_size + game_settings.field_width:
        return True
    else:
        return False

def stabilize_ship(ship):
    remainder_x = (ship.x - game_settings.border_size) % game_settings.cell_width
    remainder_y = (ship.y - game_settings.border_size) % game_settings.cell_width
    if remainder_x > 0:
        if remainder_x < (game_settings.cell_width / 2):
            ship.x -= remainder_x
        else:
            ship.x += game_settings.cell_width - remainder_x
    if remainder_y > 0:
        if remainder_y < (game_settings.cell_width / 2):
            ship.y -= remainder_y
        else:
            ship.y += game_settings.cell_width - remainder_y

def add_ship_to_field(ship, i, j, field):
    ship.cell_x = j
    ship.cell_y = i
    for k in range(0, ship.size):
        field[i][j] = 1
        if ship.is_horizontal():
            j += 1
        else:
            i += 1

def fix_ships(ships_array):
    for ship in ships_array:
        ship.fix_on_place()

#define ship coordinates for player field array
def add_ships_to_field(field, ship_array):
    for ship in ship_array:
        j,i = functions.xy_to_ji(ship.x - game_settings.border_size, ship.y - game_settings.border_size)
        # j = int((ship.x - game_settings.border_size)/game_settings.cell_width)
        # i = int((ship.y - game_settings.border_size)/game_settings.cell_width)
        if can_place_ship_here(field, i, j, ship):
            add_ship_to_field(ship, i, j, field)
        else:
            clear_field(player_field)
            raise WrongShipsPosition(j, i)

def all_ships_on_field(field, ship_array):
    for ship in ship_array:
        if not ship_on_the_field(ship):
            return False
    return True

def can_place_ship_here(field, i, j, ship):
    #check if ship
    #check if any other ship is in ship surrounding
    for n in range(i-1, i + ship.cell_height+1):
        for m in range(j-1, j + ship.cell_width+1):
            if n >= 0 and n < game_settings.cells_in_row_number:
                if m >= 0 and m < game_settings.cells_in_row_number:
                    if field[n][m] == 1:
                        return False
    return True

def randomize_field(field, ship_array):
    for ship in ship_array:
        i = random.randint(0, game_settings.cells_in_row_number - 1)
        j = random.randint(0, game_settings.cells_in_row_number - 1)
        horizontal = random.choice([True, False])
        if not horizontal:
            ship.to_vertical()
        while not (i + ship.cell_height - 1 < game_settings.cells_in_row_number
                   and j + ship.cell_width - 1 < game_settings.cells_in_row_number) \
                or not can_place_ship_here(field, i, j, ship):
            i = random.randint(0, game_settings.cells_in_row_number - 1)
            j = random.randint(0, game_settings.cells_in_row_number - 1)
        #ship.fix_on_place()
        ship.update_coordinates((game_settings.enemy_field_x + j * game_settings.cell_width,
                                game_settings.enemy_field_y + i * game_settings.cell_width))
        ship.hide()
        add_ship_to_field(ship, i, j, field)

def click_on_enemy_field(pos):
    x, y = pos
    if x >= game_settings.enemy_field_x and x <= game_settings.enemy_field_x + game_settings.field_width and \
        y >= game_settings.enemy_field_y and y <= game_settings.enemy_field_y + game_settings.field_width:
        return True
    return False

def start_enemy():
    create_ships(enemy_ship_array)
    create_field(enemy_field)
    randomize_field(enemy_field, enemy_ship_array)
    show_field(enemy_field)


def start_battle():
    fix_ships(player_ship_array)

def shoot(ij_coordinates, field, ship_array):
    j, i = ij_coordinates
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
                    return 'killed'
                return 'injured'

def update_field(field, ship_array, field_ooordinates, fire_image, missfire_image):
    for ship in ship_array:
        if ship.is_killed():
            ship.make_visible()
    for i in range(0, game_settings.cells_in_row_number):
        for j in range(0, game_settings.cells_in_row_number):
            if field[i][j] == 2:
                rect = missfire_image.get_rect()
                x, y = field_ooordinates
                plus_x, plus_y = functions.ij_to_xy(i, j)
                rect.x = x + plus_x
                rect.y = y + plus_y
                if rect not in missfire_array:
                    missfire_array.append(rect)
            if field[i][j] in (-1, -2):
                rect = fire_image.get_rect()
                x, y = field_ooordinates
                plus_x, plus_y = functions.ij_to_xy(i, j)
                rect.x = x + plus_x
                rect.y = y + plus_y
                if rect not in fire_array:
                    fire_array.append(rect)


def enemy_play():
    time.sleep(2)
    i = random.randint(0, game_settings.cells_in_row_number - 1)
    j = random.randint(0, game_settings.cells_in_row_number - 1)
    shoot_result = shoot((i, j), player_field, player_ship_array)
    if shoot_result is not 'missfire':
        enemy_play()

def draw_fire_and_missfire(screen, fire_image, missfire_image):
    for fire_rect in fire_array:
        screen.blit(fire_image, fire_rect)
    for missfire_rect in missfire_array:
        screen.blit(missfire_image, missfire_rect)

def run_game():
    #Game initialization
    pygame.init()
    screen = pygame.display.set_mode(game_settings.screen_size)
    gamer_field = Field(game_settings.player_field_coordinates)
    gamer2_field = Field(game_settings.enemy_field_coordinates)
    help_window = HelpWindow()
    start_button = Button()
    ship_dragged = None
    double_clicked = False
    battle_started = False
    create_ships(player_ship_array)
    create_field(player_field)
    pygame.display.set_caption("Battleship")
    ##start_game()
    set_start_ships_position()
    clock = pygame.time.Clock()
    offset_x = offset_y = 0
    player_turn = True
    fire_image = pygame.image.load(game_settings.fire_path)
    missfire_image = pygame.image.load(game_settings.missfire_path)
    start_enemy()
    missfire = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #if gamer performed double mouse click, turn around the ship
                    if clock.tick() < DOUBLECLICKTIME:
                        print("double click detected!")
                        double_clicked = True
                    else:
                        double_clicked = False
                    if start_button.collidepoint(event.pos) and start_button.is_clickable():
                        if all_ships_on_field(player_field, player_ship_array):
                            try:
                                add_ships_to_field(player_field, player_ship_array)
                                show_field(player_field)
                                start_button.onclick()
                                battle_started = True
                                start_battle()
                            except WrongShipsPosition:
                                print("Something wrong! Take a look at field")
                        #     ##TODO: log on helpwindow
                    for ship in player_ship_array:
                        if ship.collidepoint(event.pos) and ship.is_dragable():
                            if double_clicked:
                                ship.change_angle()
                                double_clicked = False
                            else:
                                ship_dragged = ship
                                mouse_x, mouse_y = event.pos
                                offset_x = ship.x - mouse_x
                                offset_y = ship.y - mouse_y
                    if battle_started and click_on_enemy_field(event.pos) and player_turn:
                        x, y = event.pos
                        x = x - game_settings.enemy_field_x
                        y = y - game_settings.enemy_field_y
                        shoot_result = shoot(functions.xy_to_ji(x, y), enemy_field, enemy_ship_array)
                        if shoot_result == 'missfire':
                            missfire = True
                            player_turn = False
                        show_field(enemy_field)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if ship_dragged is not None:
                        #set ship the right position and on the field
                        if ship_on_the_field(ship_dragged):
                            stabilize_ship(ship_dragged)
                        else:
                            ship_dragged.take_default_position()
                        ship_dragged = None
            elif event.type == pygame.MOUSEMOTION:
                if ship_dragged is not None:
                    mouse_x, mouse_y = event.pos
                    ship_dragged.x = mouse_x + offset_x
                    ship_dragged.y = mouse_y + offset_y
        update_field(player_field, player_ship_array, game_settings.player_field_coordinates, fire_image, missfire_image)
        update_field(enemy_field, enemy_ship_array, game_settings.enemy_field_coordinates, fire_image, missfire_image)
        screen.fill(game_settings.bg_color)
        gamer_field.update(screen)
        screen.blit(gamer_field, game_settings.player_field_coordinates)
        gamer2_field.update(screen)
        screen.blit(gamer2_field, game_settings.enemy_field_coordinates)
        help_window.update()
        screen.blit(help_window, game_settings.help_window_coordinates)
        start_button.update(screen)
        draw_ships(screen, player_ship_array)
        draw_ships(screen, enemy_ship_array)
        draw_fire_and_missfire(screen, fire_image, missfire_image)
        pygame.display.flip()
        if(missfire):
            enemy_play()
            missfire = False
            player_turn = True

run_game()

