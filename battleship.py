import sys
import pygame

from settings import Settings as game_settings
from field import Field
from help_window import HelpWindow


def run_game():
    #Game initialization
    pygame.init()
    screen = pygame.display.set_mode(game_settings.screen_size)
    field1 = Field()
    field2 = Field()
    help_window = HelpWindow()
    pygame.display.set_caption("Battleship")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(game_settings.bg_color)
        field1.update()
        screen.blit(field1, game_settings.field1_coordinates)
        field2.update()
        screen.blit(field2, game_settings.field2_coordinates)
        help_window.update()
        screen.blit(help_window, game_settings.help_window_coordinates)
        #Gamer pass
        pygame.display.flip()

run_game()