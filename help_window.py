import pygame

from settings import Settings as game_settings


class HelpWindow(pygame.Surface):
    def __init__(self):
        pygame.Surface.__init__(self, game_settings.help_window_size)

    def update(self):
        self.fill(game_settings.help_window_color)