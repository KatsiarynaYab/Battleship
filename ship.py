import pygame

from settings import Settings as game_settings

class Ship(pygame.Surface):
    def __init__(self, size = 1):
        ship_size = (game_settings.cell_width, game_settings.cell_width*size)
        pygame.Surface.__init__(self, ship_size)
