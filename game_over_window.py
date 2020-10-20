import pygame

import config
from button import YesNoButton


class GameOverWindow:
    def __init__(self):
        self.surf = pygame.Surface(config.game_over_window_size)
        self.visible = False
        self.yes = YesNoButton('Yes', config.game_over_window_coordinates[0] + 25,
                               config.game_over_window_coordinates[1] + 50)
        self.no = YesNoButton('No', config.game_over_window_coordinates[0] + 125,
                              config.game_over_window_coordinates[1] + 50)
        self.result = ''

    def set_text(self, text):
        self.result = text

    def set_visible(self, arg):
        self.visible = arg

    def update(self, screen):
        if self.visible:
            self.surf.fill(config.bg_color)
            result_sprite = pygame.font.Font(None, 40).render(self.result, True, pygame.Color("red"))
            result_rect = result_sprite.get_rect(center=(config.game_over_window_size[0] / 2, 10))
            text_sprite = pygame.font.Font(None, 20).render("Try again?", True, pygame.Color("black"))
            text_rect = result_sprite.get_rect(center=(config.game_over_window_size[0] / 2 + 25, 40))
            self.surf.blit(result_sprite, result_rect)
            self.surf.blit(text_sprite, text_rect)
            screen.blit(self.surf, config.game_over_window_coordinates)
            self.yes.update(screen)
            self.no.update(screen)
