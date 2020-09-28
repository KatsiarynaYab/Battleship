import pygame

from settings import Settings as game_settings


class Ship():
    def __init__(self, screen, size=1,):
        self.default_ship_coordinates = self.x, self.y = (0, 0)
        self.size = size
        self.screen = screen
        self.ship_body_width, self.ship_body_height = (game_settings.cell_width*self.size+1, game_settings.cell_width+1)
        ship_filename = 'ships/ship' + str(self.size) + '.png'
        self.image = pygame.image.load(ship_filename)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        self.screen.blit(self.image, self.rect)

    def update_coordinates(self, coordinates):
        self.x, self.y = coordinates

    def set_default_coordinates(self, coordinates):
        self.default_ship_coordinates = self.x, self.y = coordinates

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)

    def to_vertical(self):
        pygame.