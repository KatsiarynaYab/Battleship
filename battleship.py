import sys

import pygame

import config
import game_functions
import ships_functions
from button import StartButton, RandomizeButton
from enemy import Enemy
from field import Field
from game_errors import WrongShipsPosition
from game_over_window import GameOverWindow
from help_window import HelpWindow
from ship_panel import ShipPanel

DOUBLECLICKTIME = 500

player_ship_array = []
enemy_ship_array = []
player_field = []
enemy_field = []
fire_array = []
missfire_array = []


def start_enemy():
    game_functions.randomize_field(enemy_field, enemy_ship_array, config.enemy_field_x, config.enemy_field_y)
    ships_functions.add_ships_to_field(enemy_field, enemy_ship_array, config.enemy_field_x, config.enemy_field_y)
    ships_functions.hide_ships(enemy_ship_array)


def start_battle():
    ships_functions.fix_ships(player_ship_array)


def update_field(field, ship_array, field_ooordinates, fire_image, missfire_image):
    for ship in ship_array:
        if ship.killed:
            ship.set_visible(True)
    for i in range(0, config.cells_in_row_number):
        for j in range(0, config.cells_in_row_number):
            if field[i][j] == 2:
                rect = missfire_image.get_rect()
                x, y = field_ooordinates
                plus_x, plus_y = game_functions.ij_to_xy(i, j)
                rect.x = x + plus_x
                rect.y = y + plus_y
                if rect not in missfire_array:
                    missfire_array.append(rect)
            if field[i][j] in (-1, -2):
                rect = fire_image.get_rect()
                x, y = field_ooordinates
                plus_x, plus_y = game_functions.ij_to_xy(i, j)
                rect.x = x + plus_x
                rect.y = y + plus_y
                if rect not in fire_array:
                    fire_array.append(rect)


def draw_fire_and_missfire(screen, fire_image, missfire_image):
    for fire_rect in fire_array:
        screen.blit(fire_image, fire_rect)
    for missfire_rect in missfire_array:
        screen.blit(missfire_image, missfire_rect)


def game_over():
    if game_functions.win(enemy_ship_array) or game_functions.loose(player_ship_array):
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
                   player_ship_panel, enemy_ship_panel, game_over_window, fire_image, missfire_image):
    update_field(player_field, player_ship_array, config.player_field_coordinates, fire_image, missfire_image)
    update_field(enemy_field, enemy_ship_array, config.enemy_field_coordinates, fire_image, missfire_image)
    screen.fill(config.bg_color)
    gamer_field.update(screen)
    screen.blit(gamer_field, config.player_field_coordinates)
    gamer2_field.update(screen)
    screen.blit(gamer2_field, config.enemy_field_coordinates)
    start_button.update(screen)
    help_window.update(screen)
    randomize_button.update(screen)
    player_ship_panel.update_counters(player_ship_array)
    player_ship_panel.update(screen)
    enemy_ship_panel.update_counters(enemy_ship_array)
    enemy_ship_panel.update(screen)
    game_over_window.update(screen)
    ships_functions.draw_ships(screen, player_ship_array)
    ships_functions.draw_ships(screen, enemy_ship_array)
    draw_fire_and_missfire(screen, fire_image, missfire_image)
    pygame.display.flip()


def run_game(screen, gamer_field, gamer2_field, enemy, help_window, start_button, randomize_button, player_ship_panel,
             enemy_ship_panel, game_over_window, fire_image, missfire_image):
    ship_dragged = None
    battle_started = False
    ships_functions.set_start_player_ships_position(player_ship_array)
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
                    # if gamer performed double mouse click, turn around the ship
                    if clock.tick() < DOUBLECLICKTIME:
                        print("double click detected!")
                        double_clicked = True
                    else:
                        double_clicked = False
                    if start_button.collidepoint(event.pos) and start_button.clickable:
                        if ships_functions.all_ships_on_player_field(player_ship_array):
                            try:
                                ships_functions.add_ships_to_field(player_field, player_ship_array,
                                                                   config.player_field_coordinates[0],
                                                                   config.player_field_coordinates[1])
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
                        game_functions.randomize_field(player_field, player_ship_array,
                                                       config.player_field_coordinates[0],
                                                       config.player_field_coordinates[1])
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
                    if battle_started and game_functions.click_on_enemy_field(event.pos) and player_turn:
                        x, y = event.pos
                        x = x - config.enemy_field_x
                        y = y - config.enemy_field_y
                        shoot_result = game_functions.shoot(game_functions.xy_to_ij(x, y), enemy_field,
                                                            enemy_ship_array)
                        i, j = game_functions.xy_to_ij(x, y)
                        letter, number = game_functions.ij_to_game_coordinates(i, j)
                        if shoot_result not in ("already hit", "already missfire"):
                            help_window.add_log(f"player choose {letter}{number} \n {shoot_result}", turn_log=True)
                        if shoot_result == 'missfire':
                            missfire = True
                            player_turn = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if ship_dragged:
                        # set ship the right position and on the field
                        if ship_dragged.on_player_field():
                            ship_dragged.stabilize_ship()
                        else:
                            ship_dragged.take_default_position()
                        ship_dragged = None
            elif event.type == pygame.MOUSEMOTION:
                if ship_dragged:
                    mouse_x, mouse_y = event.pos
                    ship_dragged.x = mouse_x + offset_x
                    ship_dragged.y = mouse_y + offset_y

            help_window.update_scrollbar(screen, event)
        update_display(screen, gamer_field, gamer2_field, help_window, start_button, randomize_button,
                       player_ship_panel,
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
    if game_functions.win(enemy_ship_array):
        game_over_window.set_text('You win!!!')
    else:
        game_over_window.set_text('You loose')
    end_battle(screen, gamer_field, gamer2_field, enemy, help_window, start_button, randomize_button, player_ship_panel,
               enemy_ship_panel, game_over_window, fire_image, missfire_image)


def restart_game(screen, gamer_field, gamer2_field, enemy, help_window, start_button, randomize_button,
                 player_ship_panel,
                 enemy_ship_panel, game_over_window, fire_image, missfire_image):
    # Game initialization
    game_over_window.set_visible(False)
    game_functions.clear_field(enemy_field)
    game_functions.clear_field(player_field)
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
    run_game(screen, gamer_field, gamer2_field, enemy, help_window, start_button, randomize_button, player_ship_panel,
             enemy_ship_panel, game_over_window, fire_image, missfire_image)


def start_game():
    # Game initialization
    pygame.init()
    screen = pygame.display.set_mode(config.screen_size)
    gamer_field = Field(config.player_field_coordinates)
    gamer2_field = Field(config.enemy_field_coordinates)
    enemy = Enemy()
    ships_functions.create_ships(enemy_ship_array)
    game_functions.create_field(enemy_field)
    help_window = HelpWindow()
    start_button = StartButton()
    randomize_button = RandomizeButton()
    player_ship_panel = ShipPanel((config.player_field_x, config.player_field_y +
                                   config.field_width + config.border_size))
    enemy_ship_panel = ShipPanel((config.enemy_field_x, config.enemy_field_y +
                                  config.field_width + config.border_size))
    game_over_window = GameOverWindow()
    ships_functions.create_ships(player_ship_array)
    game_functions.create_field(player_field)
    pygame.display.set_caption("Battleship")
    fire_image = pygame.image.load(config.fire_path)
    missfire_image = pygame.image.load(config.missfire_path)
    run_game(screen, gamer_field, gamer2_field, enemy, help_window, start_button, randomize_button, player_ship_panel,
             enemy_ship_panel, game_over_window, fire_image, missfire_image)


start_game()
