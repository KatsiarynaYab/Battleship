import pygame

class Settings():
    screen_size = screen_width, screen_height =  (1200, 600)

    bg_color = (245, 245, 245)
    line_color = (12, 10, 62)
    attack_color = (255, 39, 10)
    field_color = (35, 124, 169)

    field_size = field_width, field_width = (401, 401)
    cell_size = cell_width, cell_width = (int(field_width/10), int(field_width/10))
    field1_coordinates = (50, 50)
    field2_coordinates = (screen_width-50-field_width, 50)

    help_window_size = (201, 301)
    help_window_color = (226, 213, 203)
    help_window_coordinates = (50 + field_width + 50, 200)

    ship_lines_color = (135, 198, 232)