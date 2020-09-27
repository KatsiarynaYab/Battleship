import pygame

class Settings():

    def __init__(self):
        self.screen_size = self.screen_width, self.screen_height =  (1200, 600)

        self.bg_color = (245, 245, 245)
        self.line_color = (12, 10, 62)
        self.attack_color = (255, 39, 10)
        self.field_color = (135, 198, 232)

        self.field_size = self.field_width, self.field_height = (400, 400)
        self.field1_coordinates = (50, 50)
        self.field2_coordinates = (750, 50)
