import pygame

class Settings():
    screen_size = screen_width, screen_height =  (1200, 800)
    border_size = 50
    cells_in_row_number = 10

    bg_color = (245, 245, 245)
    line_color = (12, 10, 62)
    attack_color = (255, 39, 10)
    field_color = (187, 223, 241)

    field_size = field_width, field_width = (401, 401)
    cell_size = cell_width, cell_width = (int(field_width/cells_in_row_number), int(field_width/cells_in_row_number))
    player_field_coordinates = (border_size, border_size)
    enemy_field_coordinates = enemy_field_x, enemy_field_y = (screen_width-border_size-field_width, border_size)
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

    help_window_size = (200, 300)
    help_window_color = (226, 213, 203)
    help_window_coordinates = (border_size + field_width + border_size, 150)

    start_button_size = start_button_width, start_button_height = (100, 50)
    start_button_color = (224, 26, 0)
    start_button_coordinates = start_button_x, start_button_y= (border_size + field_width + border_size*2, border_size)

    ships_path = 'images/ships/ship'
    fire_path = 'images/fire.png'
    missfire_path = 'images/cross.png'