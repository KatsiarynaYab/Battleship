import pygame

class Settings():
    screen_size = screen_width, screen_height =  (1200, 600)
    border_size = 50

    bg_color = (245, 245, 245)
    line_color = (12, 10, 62)
    attack_color = (255, 39, 10)
    field_color = (187, 223, 241)

    field_size = field_width, field_width = (401, 401)
    cell_size = cell_width, cell_width = (int(field_width/10), int(field_width/10))
    field1_coordinates = (border_size, border_size)
    field2_coordinates = (screen_width-border_size-field_width, border_size)

    help_window_size = (201, 301)
    help_window_color = (226, 213, 203)
    help_window_coordinates = (border_size + field_width + border_size, 100)
