import pygame

import config

class ShootResult():
    def __init__(self, image):
        self.coordinates = (0, 0)
        self.image = image
        self.rect = self.image.get_rect()

    def set_coordinates(self, x, y):
        self.coordinates = (x, y)

    def update(self, surface):
        self.rect.x, self.rect.y = self.coordinates
        surface.blit(self.image, self.rect)

    def __eq__(self, other):
        return self.coordinates == other.coordinates

    def __ne__(self, other):
        return self.coordinates!=other.coordinates
    
    def __hash__(self):
        return self.coordinates[0]*3 + self.coordinates[1]*5

class Fire(ShootResult):
    def __init__(self):
        self.image = pygame.image.load(config.fire_path)
        ShootResult.__init__(self, self.image)

class Missfire(ShootResult):
    def __init__(self):
        self.image = pygame.image.load(config.missfire_path)
        ShootResult.__init__(self, self.image)