import sys
import random
import pygame

import config

import ships_functions
import shoot_results
from game_errors import WrongShipsPosition


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


def start_enemy(enemy_field, enemy_ship_array):
    randomize_field(enemy_field, enemy_ship_array, config.enemy_field_x, config.enemy_field_y)
    ships_functions.add_ships_to_field(enemy_field, enemy_ship_array, config.enemy_field_x, config.enemy_field_y)
    ships_functions.hide_ships(enemy_ship_array)


def update_field(field, ship_array, field_coordinates, fire_array, missfire_array):
    for ship in ship_array:
        if ship.killed:
            ship.set_visible(True)
    for i in range(0, config.cells_in_row_number):
        for j in range(0, config.cells_in_row_number):
            if field[i][j] == 2:
                x, y = field_coordinates
                plus_x, plus_y = ij_to_xy(i, j)
                missfire = shoot_results.Missfire()
                missfire.set_coordinates(x + plus_x, y + plus_y)
                if missfire not in missfire_array:
                    missfire_array.append(missfire)
            if field[i][j] in (-1, -2):
                fire = shoot_results.Fire()
                x, y = field_coordinates
                plus_x, plus_y = ij_to_xy(i, j)
                fire.set_coordinates(x + plus_x, y + plus_y)
                if fire not in fire_array:
                    fire_array.append(fire)


def draw_fire_and_missfire(screen, fire_array, missfire_array):
    for fire in fire_array:
        fire.update(screen)
    for missfire in missfire_array:
        missfire.update(screen)


def game_over(player_ship_array, enemy_ship_array):
    if win(enemy_ship_array) or loose(player_ship_array):
        return True
    return False


def end_battle(screen, gamer_field, gamer2_field, enemy, help_window, start_button, randomize_button, player_ship_panel,
               enemy_ship_panel, game_over_window, enemy_field, player_field, fire_array,
               missfire_array, player_ship_array, enemy_ship_array):
    game_over_window.set_visible(True)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over_window.yes.collidepoint(event.pos):
                    print('yes')
                    restart_game(screen, gamer_field, gamer2_field, enemy, help_window, start_button, randomize_button,
                         player_ship_panel, enemy_ship_panel, game_over_window, enemy_field,
                         player_field, fire_array, missfire_array, player_ship_array, enemy_ship_array)
                    return
                elif game_over_window.no.collidepoint(event.pos):
                    print('no')
                    sys.exit()
        update_display(screen, gamer_field, gamer2_field, help_window, start_button, randomize_button,
                       player_ship_panel, enemy_ship_panel, game_over_window, player_field,
                       enemy_field, player_ship_array, enemy_ship_array,fire_array, missfire_array)


def update_display(screen, gamer_field, gamer2_field, help_window, start_button, randomize_button,
                   player_ship_panel, enemy_ship_panel, game_over_window, player_field,
                   enemy_field, player_ship_array, enemy_ship_array, fire_array, missfire_array):
    update_field(player_field, player_ship_array, config.player_field_coordinates, fire_array, missfire_array)
    update_field(enemy_field, enemy_ship_array, config.enemy_field_coordinates, fire_array, missfire_array)
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
    draw_fire_and_missfire(screen, fire_array, missfire_array)
    pygame.display.flip()


def restart_game(screen, gamer_field, gamer2_field, enemy, help_window, start_button, randomize_button,
                 player_ship_panel, enemy_ship_panel, game_over_window, enemy_field,
                 player_field, fire_array, missfire_array, player_ship_array, enemy_ship_array):
    # Game initialization
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
    run_game(screen, gamer_field, gamer2_field, enemy, help_window, start_button, randomize_button, player_ship_panel,
             enemy_ship_panel, game_over_window, player_ship_array, enemy_ship_array,
             player_field, enemy_field, fire_array, missfire_array)

def run_game(screen, player_map, enemy_map, enemy, help_window, start_button, randomize_button, player_ship_panel,
             enemy_ship_panel, game_over_window, player_ship_array, enemy_ship_array,
             player_field, enemy_field, fire_array, missfire_array):
    ship_dragged = None
    battle_started = False
    ships_functions.set_start_player_ships_position(player_ship_array)
    clock = pygame.time.Clock()
    offset_x = offset_y = 0
    player_turn = True
    start_enemy(enemy_field, enemy_ship_array)
    missfire = False
    while not game_over(player_ship_array, enemy_ship_array):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # if gamer performed double mouse click, turn around the ship
                    if clock.tick() < config.DOUBLECLICKTIME:
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
                                ships_functions.fix_ships(player_ship_array)
                                battle_started = True
                                help_window.add_log('!!!Battle started!!!')
                            except WrongShipsPosition:
                                help_window.add_log('"Something wrong! Take a look at field"')
                    if randomize_button.collidepoint(event.pos) and randomize_button.clickable:
                        randomize_field(player_field, player_ship_array,
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
                    if battle_started and click_on_enemy_field(event.pos) and player_turn:
                        x, y = event.pos
                        x = x - config.enemy_field_x
                        y = y - config.enemy_field_y
                        shoot_result = shoot(xy_to_ij(x, y), enemy_field, enemy_ship_array)
                        if shoot_result not in ("already hit", "already missfire"):
                            i, j = xy_to_ij(x, y)
                            letter, number = ij_to_game_coordinates(i, j)
                            help_window.add_log(f"player choose {letter}{number} \n {shoot_result}", turn_log=True)
                        if shoot_result == 'missfire':
                            missfire = True
                            player_turn = False
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if ship_dragged:
                        # set ship the right position on the field
                        if ship_dragged.on_player_field():
                            ship_dragged.stabilize_on_player_field()
                        else:
                            ship_dragged.take_default_position()
                        ship_dragged = None
            elif event.type == pygame.MOUSEMOTION:
                if ship_dragged:
                    mouse_x, mouse_y = event.pos
                    ship_dragged.x = mouse_x + offset_x
                    ship_dragged.y = mouse_y + offset_y

            help_window.update_scrollbar(event)
        update_display(screen, player_map, enemy_map, help_window, start_button, randomize_button,
                       player_ship_panel, enemy_ship_panel, game_over_window, player_field,
                       enemy_field, player_ship_array, enemy_ship_array, fire_array, missfire_array)
        if missfire:
            enemy.turn(player_field, player_ship_array, help_window)
            update_display(screen, player_map, enemy_map, help_window, start_button, randomize_button,
                           player_ship_panel, enemy_ship_panel, game_over_window,
                           player_field, enemy_field, player_ship_array, enemy_ship_array, fire_array, missfire_array)
            while not enemy.missfire and not game_over(player_ship_array, enemy_ship_array):
                enemy.turn(player_field, player_ship_array, help_window)
                update_display(screen, player_map, enemy_map, help_window, start_button, randomize_button,
                               player_ship_panel, enemy_ship_panel, game_over_window, player_field,
                               enemy_field, player_ship_array, enemy_ship_array, fire_array, missfire_array)
            missfire = False
            player_turn = True
    if win(enemy_ship_array):
        game_over_window.set_text('You win!!!')
    else:
        game_over_window.set_text('You loose')
    end_battle(screen, player_map, enemy_map, enemy, help_window, start_button, randomize_button, player_ship_panel,
               enemy_ship_panel, game_over_window, enemy_field, player_field, fire_array,
               missfire_array, player_ship_array, enemy_ship_array)

