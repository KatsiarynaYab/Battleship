import pygame

class Settings():
    screen_size = screen_width, screen_height =  (1200, 600)
    border_size = 50
    cells_in_row_number = 10

    bg_color = (245, 245, 245)
    line_color = (12, 10, 62)
    attack_color = (255, 39, 10)
    field_color = (187, 223, 241)

    field_size = field_width, field_width = (401, 401)
    cell_size = cell_width, cell_width = (int(field_width/cells_in_row_number), int(field_width/cells_in_row_number))
    player_field_coordinates = player_field_x, player_field_y = (border_size, border_size)
    enemy_field_coordinates = enemy_field_x, enemy_field_y = (screen_width-border_size-field_width, border_size)
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    help_window_size = (200, 300)
    help_window_color = (226, 213, 203)
    help_window_coordinates = (border_size + field_width + border_size, 150)
    battleship_rules_text = "The object of Battleship is to try and sink all of the other player's ships before " \
                            "they sink all of yours. All of the other player's ships are somewhere on " \
                            "his/her board. You try and hit them by clicking on one of the squares" \
                            " on the board. The other player also tries to hit your ships by choosing coordinates." \
                            " Neither you nor the other player can see the other's board so you must try" \
                            " to guess where they are. Each player places 10 ships somewhere on their board.  " \
                            "The ships can only be placed vertically or horizontally. No part of a ship may hang off " \
                            "the edge of the board. Ships may not overlap or touch each other. Once the guessing " \
                            "begins, the players may not move the ships.\nHint: perform doubleclick on ship to rotate it"
    help_window_font_size = 19
    scrollbar_size = (20, 40)

    start_button_size = start_button_width, start_button_height = (100, 50)
    start_button_color = (224, 26, 0)
    start_button_coordinates = start_button_x, start_button_y= (border_size + field_width + border_size*2, border_size)

    random_button_size = random_button_width, random_button_height = (200, 30)
    random_button_color = (65, 105, 225)
    random_button_coordinates = random_button_x, random_button_y = (help_window_coordinates[0],
                                                                    help_window_coordinates[1] - 40)

    ships_path = 'images/ships/ship'
    fire_path = 'images/fire.png'
    missfire_path = 'images/cross.png'

    game_over_window_size = (200, 90)
    game_over_window_color = (192,192,192)
    game_over_window_coordinates = (help_window_coordinates[0], border_size)

    ship_panel_size = (field_width + border_size, 200)