import pygame

import config
from functions import ships_functions
from game_elements.ship import Ship


class ShipPanel:
    def __init__(self, coordinates):
        self.__surface = pygame.Surface(config.ship_panel_size)
        self.coordinates = coordinates
        self.width = config.ship_panel_size[0]
        self.height = config.ship_panel_size[1]
        self.visible = False
        self._ships = []
        self.__ships_counter = [4, 3, 2, 1]
        self.__counter_rects = []
        self.__font = pygame.font.Font(None, 40)
        for i in range(1, 5):
            self._ships.append(Ship(i))
        margine = 70
        x = 0
        y = 0
        i = 0
        for ship in self._ships:
            ship.update_coordinates((x, y))
            text_sprite = self.__font.render("x " + str(self.__ships_counter[i]), True, pygame.Color("black"))
            rect = text_sprite.get_rect()
            rect.x = x + ship.cell_width * config.cell_width + 10
            rect.y = y
            self.__counter_rects.append(rect)
            x += ship.cell_width * config.cell_width + margine
            i += 1
            if i == 3:
                y = config.border_size
                x = 0

    def update_counters(self, ship_array):
        self.__ships_counter = ships_functions.count_ships(ship_array)

    def update(self, screen):
        if self.visible:
            self.__surface.fill(config.bg_color)
            for i in range(0, 4):
                text_sprite = self.__font.render("x " + str(self.__ships_counter[i]), True, pygame.Color("black"))
                self.__surface.blit(text_sprite, self.__counter_rects[i])
            ships_functions.draw_ships(self.__surface, self._ships)
            screen.blit(self.__surface, self.coordinates)

    def set_visible(self, arg):
        self.visible = arg
