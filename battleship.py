import sys
import pygame

from settings import Settings as game_settings
from field import Field
from help_window import HelpWindow
from ship import Ship

ship_array = []

def create_ships(screen):
    ship_array.append(Ship(screen, 4))
    for i in range(0, 2):
        ship_array.append(Ship(screen, 3))
    for i in range(0, 3):
        ship_array.append(Ship(screen, 2))
    for i in range(0, 4):
        ship_array.append(Ship(screen, 1))


def start_game():
    #Set start position to ships
    coordinates = (50, 500)
    switch_to_second_line = False
    for ship in ship_array:
        ship.update_coordinates(coordinates)
        coordinates = (coordinates[0] + 50 + game_settings.cell_width*ship.size, coordinates[1])
        #switch to second line
        if coordinates[0] > 700 and switch_to_second_line == False:
            coordinates = (50, 550)
            switch_to_second_line = True


def draw_ships(screen):
    for ship in ship_array:
        ship.update()


def run_game():
    #Game initialization
    pygame.init()
    screen = pygame.display.set_mode(game_settings.screen_size)
    gamer_field = Field()
    enemy_field = Field()
    help_window = HelpWindow()
    create_ships(screen)
    # for ship in ship_array:
    #     print("ship of size " + str(ship_array[i].size) + " added")
    pygame.display.set_caption("Battleship")
    start_game()
    ship_draging = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     if event.button == 1:
            #         if ship_array[0].collidepoint(event.pos):
            #             ship_draging = True
            #             mouse_x, mouse_y = event.pos
            #             offset_x = ship_array[0].x - mouse_x
            #             offset_y = ship_array[0].y - mouse_y
            # elif event.type == pygame.MOUSEBUTTONUP:
            #     if event.button == 1:
            #         ship_draging = False
            # elif event.type == pygame.MOUSEMOTION:
            #     if ship_draging:
            #         mouse_x, mouse_y = event.pos
            #         ship_array[0].x = mouse_x + offset_x
            #         ship_array[0].y = mouse_y + offset_y
        screen.fill(game_settings.bg_color)
        gamer_field.update()
        screen.blit(gamer_field, game_settings.field1_coordinates)
        enemy_field.update()
        screen.blit(enemy_field, game_settings.field2_coordinates)
        help_window.update()
        screen.blit(help_window, game_settings.help_window_coordinates)
        draw_ships(screen)
        #Gamer pass
        pygame.display.flip()


run_game()

