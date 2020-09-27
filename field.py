import pygame
from settings import Settings as game_settings


class Field(pygame.Surface):
    def __init__(self):
        pygame.Surface.__init__(self, game_settings.field_size)

    def update(self):
        self.fill(game_settings.field_color)
        #Draw borders and grid
        for i in range(0, game_settings.field_width, int(game_settings.field_width/10)):
            pygame.draw.line(self, game_settings.line_color, (i, 0), (i, game_settings.field_width)) #vertical
            pygame.draw.line(self, game_settings.line_color, (0, i), (game_settings.field_width, i))  # horizontal