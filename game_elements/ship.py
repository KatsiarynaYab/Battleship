import pygame

import config


class Ship:
    def __init__(self, size=1, ):
        self.default_ship_coordinates = self.x, self.y = (0, 0)
        self.size = size
        self.lifes = size
        self.horizontal = True
        self._ship_body_width, self._ship_body_height = (config.cell_width * self.size + 1, config.cell_width + 1)
        ship_filename = config.ships_path + str(self.size) + '.png'
        self.__image = pygame.image.load(ship_filename)
        self.__rect = self.__image.get_rect()
        self.cell_width = self.size
        self.cell_height = 1
        self.cell_x = self.cell_y = 0
        self.dragable = True
        self.killed = False
        self.visible = True

    def update(self, screen):
        self.__rect.x = self.x
        self.__rect.y = self.y
        screen.blit(self.__image, self.__rect)

    def update_coordinates(self, coordinates):
        self.x, self.y = coordinates

    def set_default_coordinates(self, coordinates):
        self.default_ship_coordinates = self.x, self.y = coordinates

    def collidepoint(self, pos):
        return self.__rect.collidepoint(pos)

    def set_horizontal(self, arg):
        self.horizontal = arg

    def alive(self):
        self.lifes = self.size
        self.killed = False

    def change_angle(self):
        if self.horizontal:
            self.to_vertical()
        else:
            self.to_horizontal()

    def to_vertical(self):
        tmp = self.__rect.width
        self.__rect.width = self._ship_body_width = self.__rect.height
        self.__rect.height = self._ship_body_height = tmp
        self.__image = pygame.transform.rotate(self.__image, 90)
        self.cell_width = 1
        self.cell_height = self.size
        self.horizontal = False

    def to_horizontal(self):
        tmp = self.__rect.width
        self.__rect.width = self._ship_body_width = self.__rect.height
        self.__rect.height = self._ship_body_height = tmp
        self.__image = pygame.transform.rotate(self.__image, -90)
        self.cell_width = self.size
        self.cell_height = 1
        self.horizontal = True

    def take_default_position(self):
        self.x, self.y = self.default_ship_coordinates
        if not self.horizontal:
            self.change_angle()

    def hide(self):
        self.visible = False

    def set_visible(self, arg):
        self.visible = arg

    def set_dragable(self, arg):
        self.dragable = arg

    def fix_on_place(self):
        self.set_dragable(False)

    def shoot(self, i, j):
        pass

    def injured(self, i, j):
        for n in range(self.cell_y, self.cell_y + self.cell_height):
            for m in range(self.cell_x, self.cell_x + self.cell_width):
                if (n, m) == (i, j):
                    self.lifes -= 1
                    if self.lifes == 0:
                        self.killed = True
                    return True
        return False

    def on_player_field(self):
        optimizer = config.cell_width / 2
        if self.x + optimizer > config.border_size and self.y + optimizer > config.border_size \
                and self.x + self._ship_body_width - optimizer < config.border_size + config.field_width \
                and self.y + self._ship_body_height - optimizer < config.border_size + config.field_width:
            return True
        else:
            return False

    def stabilize_on_player_field(self):
        remainder_x = (self.x - config.border_size) % config.cell_width
        remainder_y = (self.y - config.border_size) % config.cell_width
        if remainder_x > 0:
            if remainder_x < (config.cell_width / 2):
                self.x -= remainder_x
            else:
                self.x += config.cell_width - remainder_x
        if remainder_y > 0:
            if remainder_y < (config.cell_width / 2):
                self.y -= remainder_y
            else:
                self.y += config.cell_width - remainder_y
