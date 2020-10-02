import sys
import pygame

from settings import Settings as game_settings
from field import Field
from help_window import HelpWindow
from ship import Ship
from button import Button

DOUBLECLICKTIME = 500

ship_array = []
player_field = []

debug_field = [[0, 0, 1, 1, ]]

def create_ships(screen):
    ship_array.append(Ship(screen, 4))
    for i in range(0, 2):
        ship_array.append(Ship(screen, 3))
    for i in range(0, 3):
        ship_array.append(Ship(screen, 2))
    for i in range(0, 4):
        ship_array.append(Ship(screen, 1))

def create_player_field():
    for i in range(0, game_settings.cells_in_row_number):
        player_field.append([])
        for j in range(0, game_settings.cells_in_row_number):
            player_field[i].append(0)

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
def show_player_field():
    for i in player_field:
        for j in i:
            print(j, end = ' ')
        print('\n')
    print('\n')

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

#define ship coordinates for player field array
#returnes false if something wrong
#TODO: add exception handle
def add_ships_to_field(field):
    for ship in ship_array:
        j = int((ship.x - game_settings.border_size)/game_settings.cell_width)
        i = int((ship.y - game_settings.border_size)/game_settings.cell_width)
        if can_place_ship_here(field, i, j, ship):
            ship.fix_on_place()
            for k in range(0, ship.size):
                field[i][j] = 1
                if ship.is_horizontal():
                    j += 1
                else:
                    i += 1
        else:
            pass
        ##TODO: ecxeption

def all_ships_on_field(field):
    for ship in ship_array:
        if not ship_on_the_field(ship):
            return False
    return True

def can_place_ship_here(field, x, y, ship):
    #check ship surrounding
    #check_top
    for i in range(x-1, x + ship.cell_height+1):
        for j in range(y-1, y + ship.cell_width+1):
            if i > 0 and i < game_settings.cells_in_row_number:
                if j > 0 and j < game_settings.cells_in_row_number:
                    if player_field[i][j] == 1:
                        return False
    return True

def randomize_field():
    

def enemy_turn():
    pass


def start_battle():
    pass

def run_game():
    #Game initialization
    pygame.init()
    screen = pygame.display.set_mode(game_settings.screen_size)
    gamer_field = Field(game_settings.player_field_coordinates)
    enemy_field = Field(game_settings.enemy_field_coordinates)
    help_window = HelpWindow()
    start_button = Button()
    ship_dragged = None
    double_clicked = False
    create_ships(screen)
    create_player_field()
    pygame.display.set_caption("Battleship")
    start_game()
    clock = pygame.time.Clock()

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
                        if all_ships_on_field(player_field):
                            add_ships_to_field(player_field)
                            show_player_field()
                            start_button.onclick()
                            start_battle()
                        #     ##TODO: log on helpwindow
                    for ship in ship_array:
                        if ship.collidepoint(event.pos) and ship.is_dragable():
                            if double_clicked:
                                ship.change_angle()
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
                            stabilize_ship(ship_dragged)
                        else:
                            ship_dragged.take_default_position()
                        ship_dragged = None
            elif event.type == pygame.MOUSEMOTION:
                if ship_dragged is not None:
                    mouse_x, mouse_y = event.pos
                    ship_dragged.x = mouse_x + offset_x
                    ship_dragged.y = mouse_y + offset_y
        screen.fill(game_settings.bg_color)
        gamer_field.update(screen)
        screen.blit(gamer_field, game_settings.player_field_coordinates)
        enemy_field.update(screen)
        screen.blit(enemy_field, game_settings.enemy_field_coordinates)
        help_window.update()
        screen.blit(help_window, game_settings.help_window_coordinates)
        start_button.update(screen)
        draw_ships(screen)
        pygame.display.flip()


run_game()

