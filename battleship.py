import sys
import pygame
import random
import time

import functions as func

from settings import Settings as game_settings
from enemy import Enemy
from game_errors import WrongShipsPosition
from field import Field
from help_window import HelpWindow
from ship import Ship
from button import StartButton, RandomizeButton
from ship_panel import ShipPanel
from game_over_window import GameOverWindow

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
    for i in range(0, len(field)):
        for j in range(0, len(field[i])):
            field[i][j] = 0


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
        if ship.visible:
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
        if ship.horizontal:
            j += 1
        else:
            i += 1

def fix_ships(ships_array):
    for ship in ships_array:
        ship.fix_on_place()

#define ship coordinates for player field array
def add_ships_to_field(field, ship_array, field_x, field_y):
    for ship in ship_array:
        i, j = func.xy_to_ij(ship.x - field_x, ship.y - field_y)
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
            if func.correct_coordinates(n, m):
                if field[n][m] == 1:
                    return False
    return True

def randomize_field(field, ship_array, field_x, field_y):
    for ship in ship_array:
        i = random.randint(0, game_settings.cells_in_row_number - 1)
        j = random.randint(0, game_settings.cells_in_row_number - 1)
        horizontal = random.choice([True, False])
        if not horizontal:
            ship.change_angle()
        while not (i + ship.cell_height - 1 < game_settings.cells_in_row_number
                   and j + ship.cell_width - 1 < game_settings.cells_in_row_number) \
                or not can_place_ship_here(field, i, j, ship):
            i = random.randint(0, game_settings.cells_in_row_number - 1)
            j = random.randint(0, game_settings.cells_in_row_number - 1)
        #ship.fix_on_place()
        ship.update_coordinates((field_x + j * game_settings.cell_width,
                                field_y + i * game_settings.cell_width))
        add_ship_to_field(ship, i, j, field)
    clear_field(field)

def hide_ships(ship_array):
    for ship in ship_array:
        ship.hide()

def click_on_enemy_field(pos):
    x, y = pos
    if x >= game_settings.enemy_field_x and x <= game_settings.enemy_field_x + game_settings.field_width and \
        y >= game_settings.enemy_field_y and y <= game_settings.enemy_field_y + game_settings.field_width:
        return True
    return False

def start_enemy():
    randomize_field(enemy_field, enemy_ship_array, game_settings.enemy_field_x, game_settings.enemy_field_y)
    add_ships_to_field(enemy_field, enemy_ship_array, game_settings.enemy_field_x, game_settings.enemy_field_y)
    hide_ships(enemy_ship_array)
    show_field(enemy_field)


def start_battle():
    fix_ships(player_ship_array)


def update_field(field, ship_array, field_ooordinates, fire_image, missfire_image):
    for ship in ship_array:
        if ship.killed:
            ship.set_visible(True)
    for i in range(0, game_settings.cells_in_row_number):
        for j in range(0, game_settings.cells_in_row_number):
            if field[i][j] == 2:
                rect = missfire_image.get_rect()
                x, y = field_ooordinates
                plus_x, plus_y = func.ij_to_xy(i, j)
                rect.x = x + plus_x
                rect.y = y + plus_y
                if rect not in missfire_array:
                    missfire_array.append(rect)
            if field[i][j] in (-1, -2):
                rect = fire_image.get_rect()
                x, y = field_ooordinates
                plus_x, plus_y = func.ij_to_xy(i, j)
                rect.x = x + plus_x
                rect.y = y + plus_y
                if rect not in fire_array:
                    fire_array.append(rect)


def draw_fire_and_missfire(screen, fire_image, missfire_image):
    for fire_rect in fire_array:
        screen.blit(fire_image, fire_rect)
    for missfire_rect in missfire_array:
        screen.blit(missfire_image, missfire_rect)

def win():
    for ship in enemy_ship_array:
        if not ship.killed:
            return False
    return True

def loose():
    for ship in player_ship_array:
        if not ship.killed:
            return False
    return True

def game_over():
    if win() or loose():
        return True
    return False

def end_battle(screen, gamer_field, gamer2_field, enemy, help_window, start_button, randomize_button, player_ship_panel,
             enemy_ship_panel, game_over_window, fire_image, missfire_image):
    game_over_window.set_visible(True)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over_window.yes.collidepoint(event.pos):
                    print('yes')
                    restart_game(screen, gamer_field, gamer2_field, enemy, help_window, start_button, randomize_button,
                                player_ship_panel, enemy_ship_panel, game_over_window, fire_image, missfire_image)
                    return
                elif game_over_window.no.collidepoint(event.pos):
                    print('no')
                    sys.exit()
        update_display(screen, gamer_field, gamer2_field, help_window, start_button, randomize_button,
                           player_ship_panel, enemy_ship_panel, game_over_window, fire_image, missfire_image)



def update_display(screen, gamer_field, gamer2_field, help_window, start_button, randomize_button,
                   player_ship_panel, enemy_ship_panel, game_over_window, fire_image, missfire_image, event = None):
    update_field(player_field, player_ship_array, game_settings.player_field_coordinates, fire_image, missfire_image)
    update_field(enemy_field, enemy_ship_array, game_settings.enemy_field_coordinates, fire_image, missfire_image)
    screen.fill(game_settings.bg_color)
    gamer_field.update(screen)
    screen.blit(gamer_field, game_settings.player_field_coordinates)
    gamer2_field.update(screen)
    screen.blit(gamer2_field, game_settings.enemy_field_coordinates)
    start_button.update(screen)
    help_window.update(screen)
    randomize_button.update(screen)
    player_ship_panel.update_counters(player_ship_array)
    player_ship_panel.update(screen)
    enemy_ship_panel.update_counters(enemy_ship_array)
    enemy_ship_panel.update(screen)
    game_over_window.update(screen)
    draw_ships(screen, player_ship_array)
    draw_ships(screen, enemy_ship_array)
    draw_fire_and_missfire(screen, fire_image, missfire_image)
    pygame.display.flip()

def run_game(screen, gamer_field, gamer2_field, enemy, help_window, start_button, randomize_button, player_ship_panel,
             enemy_ship_panel, game_over_window, fire_image, missfire_image):
    ship_dragged = None
    double_clicked = False
    battle_started = False
    set_start_ships_position()
    clock = pygame.time.Clock()
    offset_x = offset_y = 0
    player_turn = True
    start_enemy()
    missfire = False
    while not game_over():
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
                    if start_button.collidepoint(event.pos) and start_button.clickable:
                        if all_ships_on_field(player_field, player_ship_array):
                            try:
                                add_ships_to_field(player_field, player_ship_array,
                                                   game_settings.player_field_coordinates[0],
                                                   game_settings.player_field_coordinates[1])
                                #show_field(player_field)
                                start_button.set_clickable(False)
                                randomize_button.set_clickable(False)
                                player_ship_panel.set_visible(True)
                                enemy_ship_panel.set_visible(True)
                                battle_started = True
                                start_battle()
                                help_window.add_log('!!!Battle started!!!')
                            except WrongShipsPosition:
                                help_window.add_log('"Something wrong! Take a look at field"')
                    if randomize_button.collidepoint(event.pos) and randomize_button.clickable:
                        randomize_field(player_field, player_ship_array, game_settings.player_field_coordinates[0],
                                        game_settings.player_field_coordinates[1])
                    for ship in player_ship_array:
                        if ship.collidepoint(event.pos) and ship.dragable:
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
                        shoot_result = func.shoot(func.xy_to_ij(x, y), enemy_field, enemy_ship_array)
                        i, j = func.xy_to_ij(x, y)
                        letter, number = func.ij_to_game_coordinates(i, j)
                        if shoot_result not in("already injured", "already missfire"):
                            help_window.add_log(f"player choose {letter}{number} \n {shoot_result}", turn_log=True)
                        if shoot_result == 'missfire':
                            missfire = True
                            player_turn = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if ship_dragged:
                        #set ship the right position and on the field
                        if ship_on_the_field(ship_dragged):
                            stabilize_ship(ship_dragged)
                        else:
                            ship_dragged.take_default_position()
                        ship_dragged = None
            elif event.type == pygame.MOUSEMOTION:
                if ship_dragged:
                    mouse_x, mouse_y = event.pos
                    ship_dragged.x = mouse_x + offset_x
                    ship_dragged.y = mouse_y + offset_y

            help_window.update_scrollbar(screen, event)
        update_display(screen, gamer_field, gamer2_field, help_window, start_button, randomize_button, player_ship_panel,
             enemy_ship_panel, game_over_window, fire_image, missfire_image)
        if missfire:
            enemy.turn(player_field, player_ship_array, help_window)
            update_display(screen, gamer_field, gamer2_field, help_window, start_button, randomize_button,
                           player_ship_panel, enemy_ship_panel, game_over_window, fire_image, missfire_image)
            while not enemy.missfire and not game_over():
                enemy.turn(player_field, player_ship_array, help_window)
                update_display(screen, gamer_field, gamer2_field, help_window, start_button, randomize_button,
                               player_ship_panel, enemy_ship_panel, game_over_window, fire_image, missfire_image)
            missfire = False
            player_turn = True
    if win():
        game_over_window.set_text('You win!!!')
    else:
        game_over_window.set_text('You loose')
    end_battle(screen, gamer_field, gamer2_field, enemy, help_window, start_button, randomize_button,player_ship_panel,
             enemy_ship_panel, game_over_window, fire_image, missfire_image)

def restart_game(screen, gamer_field, gamer2_field, enemy, help_window, start_button, randomize_button,player_ship_panel,
             enemy_ship_panel, game_over_window, fire_image, missfire_image):
    #Game initialization
    game_over_window.set_visible(False)
    clear_field(enemy_field)
    clear_field(player_field)
    fire_array.clear()
    missfire_array.clear()
    randomize_button.set_clickable(True)
    start_button.set_clickable(True)
    player_ship_panel.set_visible(False)
    enemy_ship_panel.set_visible(False)
    help_window.return_to_default()
    for ship in player_ship_array:
        ship.alive()
        ship.set_dragable(True)
        if not ship.horizontal:
            ship.change_angle()
    for ship in enemy_ship_array:
        ship.alive()
        if not ship.horizontal:
            ship.change_angle()
    run_game(screen, gamer_field, gamer2_field, enemy, help_window, start_button, randomize_button,player_ship_panel,
             enemy_ship_panel, game_over_window, fire_image, missfire_image)

def start_game():
    #Game initialization
    pygame.init()
    screen = pygame.display.set_mode(game_settings.screen_size)
    gamer_field = Field(game_settings.player_field_coordinates)
    gamer2_field = Field(game_settings.enemy_field_coordinates)
    enemy = Enemy()
    create_ships(enemy_ship_array)
    create_field(enemy_field)
    help_window = HelpWindow()
    start_button = StartButton()
    randomize_button = RandomizeButton()
    player_ship_panel = ShipPanel((game_settings.player_field_x, game_settings.player_field_y +
                                  game_settings.field_width + game_settings.border_size))
    enemy_ship_panel = ShipPanel((game_settings.enemy_field_x, game_settings.enemy_field_y +
                                  game_settings.field_width + game_settings.border_size))
    game_over_window = GameOverWindow()
    create_ships(player_ship_array)
    create_field(player_field)
    pygame.display.set_caption("Battleship")
    fire_image = pygame.image.load(game_settings.fire_path)
    missfire_image = pygame.image.load(game_settings.missfire_path)
    run_game(screen, gamer_field, gamer2_field, enemy, help_window, start_button, randomize_button, player_ship_panel,
             enemy_ship_panel, game_over_window, fire_image, missfire_image)

start_game()


