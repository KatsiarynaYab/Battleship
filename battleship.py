import pygame

import config
import game_functions
import ships_functions
from button import StartButton, RandomizeButton
from enemy import Enemy
from map import Map
from game_over_window import GameOverWindow
from help_window import HelpWindow
from ship_panel import ShipPanel


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
    fire_image = pygame.image.load(config.fire_path)
    missfire_image = pygame.image.load(config.missfire_path)
    game_functions.run_game(screen, player_map, enemy_map, enemy, help_window, start_button, randomize_button, player_ship_panel,
             enemy_ship_panel, game_over_window, fire_image, missfire_image, player_ship_array, enemy_ship_array, player_field,
                            enemy_field, fire_array, missfire_array)


start_game()
