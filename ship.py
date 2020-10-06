import pygame

from settings import Settings as game_settings


class Ship():
    def __init__(self, size=1,):
        self.default_ship_coordinates = self.x, self.y = (0, 0)
        self.size = size
        self.lifes = size
        self.ishorizontal = True
        self.ship_body_width, self.ship_body_height = (game_settings.cell_width*self.size+1, game_settings.cell_width+1)
        ship_filename = game_settings.ships_path + str(self.size) + '.png'
        self.image = pygame.image.load(ship_filename)
        self.rect = self.image.get_rect()
        self.cell_width = self.size
        self.cell_height = 1
        self.cell_x = self.cell_y = 0
        self.dragable = True
        self.killed = False
        self.visible = True

    def update(self, screen):
        self.rect.x = self.x
        self.rect.y = self.y
        screen.blit(self.image, self.rect)

    def update_coordinates(self, coordinates):
        self.x, self.y = coordinates

    def set_default_coordinates(self, coordinates):
        self.default_ship_coordinates = self.x, self.y = coordinates

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)

    def change_angle(self):
        if self.ishorizontal:
            self.to_vertical()
        else:
            self.to_horizontal()

    def to_vertical(self):
        tmp = self.rect.width
        self.rect.width = self.ship_body_width= self.rect.height
        self.rect.height = self.ship_body_height = tmp
        self.image = pygame.transform.rotate(self.image, 90)
        self.cell_width = 1
        self.cell_height = self.size
        self.ishorizontal = False

    def to_horizontal(self):
        tmp = self.rect.width
        self.rect.width = self.ship_body_width= self.rect.height
        self.rect.height = self.ship_body_height = tmp
        self.image = pygame.transform.rotate(self.image, -90)
        self.cell_width = self.size
        self.cell_height = 1
        self.ishorizontal = True

    def take_default_position(self):
        self.x, self.y = self.default_ship_coordinates
        if not self.ishorizontal:
            self.change_angle()

    def hide(self):
        self.visible = False

    def make_visible(self):
        self.visible = True

    def is_horizontal(self):
        return self.ishorizontal

    def is_dragable(self):
        return self.dragable

    def fix_on_place(self):
        self.dragable = False

    def shoot(self, i, j):
        pass

    def is_injured(self, i, j):
        for n in range(self.cell_y, self.cell_y+self.cell_height):
            for m in range(self.cell_x, self.cell_x+self.cell_width):
                if (n, m) == (i, j):
                    self.lifes -=1
                    if self.lifes == 0:
                        self.killed = True
                    return True
        return False

    def is_killed(self):
        return self.killed

    def is_visible(self):
        return self.visible