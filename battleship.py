import pygame

import config
from functions import game_functions, ships_functions
from controllers.button import StartButton, RandomizeButton
from game_elements.enemy import Enemy
from game_elements.map import Map
from controllers.game_over_window import GameOverWindow
from controllers.help_window import HelpWindow
from controllers.ship_panel import ShipPanel


def start_game():
    # Game initialization
    player_ship_array = []
    enemy_ship_array = []
    player_field = []
    enemy_field = []
    fire_array = []
    missfire_array = []
    pygame.init()
    screen = pygame.display.set_mode(config.screen_size)
    player_map = Map(config.player_field_coordinates)
    enemy_map = Map(config.enemy_field_coordinates)
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
    game_functions.run_game(screen, player_map, enemy_map, enemy, help_window, start_button, randomize_button,
                            player_ship_panel, enemy_ship_panel, game_over_window, player_ship_array, enemy_ship_array,
                            player_field, enemy_field, fire_array, missfire_array)


start_game()
