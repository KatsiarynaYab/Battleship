import sys
import pygame

from settings import Settings

def run_game():
    #Game initialization
    pygame.init()
    game_settings = Settings()
    screen = pygame.display.set_mode(game_settings.screen_size)
    field1 = pygame.Surface(game_settings.field_size)
    field2 = pygame.Surface(game_settings.field_size)
    pygame.display.set_caption("Battleship")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(game_settings.bg_color)
        field1.fill(game_settings.field_color)
        screen.blit(field1, game_settings.field1_coordinates)
        field2.fill(game_settings.field_color)
        screen.blit(field2, game_settings.field2_coordinates)
        #Gamer pass
        pygame.display.flip()

run_game()