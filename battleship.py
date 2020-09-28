import sys
import pygame

from settings import Settings as game_settings
from field import Field
from help_window import HelpWindow
from ship import Ship

DOUBLECLICKTIME = 500

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
    y = game_settings.border_size + game_settings.field_width + game_settings.border_size
    coordinates = (game_settings.border_size, y)
    switch_to_second_line = False
    for ship in ship_array:
        ship.set_default_coordinates(coordinates)
        coordinates = (coordinates[0] + game_settings.border_size + game_settings.cell_width*ship.size, coordinates[1])
        #switch to second line
        if coordinates[0] > 700 and switch_to_second_line == False:
            coordinates = (game_settings.border_size, y + game_settings.border_size)
            switch_to_second_line = True


def draw_ships(screen):
    for ship in ship_array:
        ship.update()

def ship_on_the_field(ship):
    optimizer = game_settings.cell_width/2
    if ship.x + optimizer > game_settings.border_size and ship.y + optimizer > game_settings.border_size \
            and ship.x + ship.ship_body_width - optimizer < game_settings.border_size + game_settings.field_width \
            and ship.y + ship.ship_body_height - optimizer < game_settings.border_size + game_settings.field_width:
        return True
    else:
        return False

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
    clock = pygame.time.Clock()
    ship_dragged = None
    mouse_click = False
    double_clicked = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #if gamer performed double mouse click, turn around the ship
                    if clock.tick() < DOUBLECLICKTIME and mouse_click:
                        print("double click detected!")
                        double_clicked = True
                    else:
                        mouse_click = False
                    mouse_click = True
                    for ship in ship_array:
                        if ship.collidepoint(event.pos):
                            if double_clicked:

                                double_clicked = False
                            else:
                                ship_dragged = ship
                                mouse_x, mouse_y = event.pos
                                offset_x = ship.x - mouse_x
                                offset_y = ship.y - mouse_y
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if ship_dragged is not None:
                        #set ship the right position and on the field
                        if ship_on_the_field(ship_dragged):
                            remainder_x = (ship_dragged.x - game_settings.border_size) % game_settings.cell_width
                            remainder_y = (ship_dragged.y - game_settings.border_size) % game_settings.cell_width
                            if remainder_x > 0:
                                if remainder_x < (game_settings.cell_width/2):
                                    ship_dragged.x -= remainder_x
                                else:
                                    ship_dragged.x += game_settings.cell_width - remainder_x
                            if remainder_y > 0:
                                if remainder_y < (game_settings.cell_width / 2):
                                    ship_dragged.y -= remainder_y
                                else:
                                    ship_dragged.y += game_settings.cell_width - remainder_y
                        else:
                            ship_dragged.x, ship_dragged.y = ship_dragged.default_ship_coordinates
                        ship_dragged = None

            elif event.type == pygame.MOUSEMOTION:
                if ship_dragged is not None:
                    mouse_x, mouse_y = event.pos
                    ship_dragged.x = mouse_x + offset_x
                    ship_dragged.y = mouse_y + offset_y
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

