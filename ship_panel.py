import pygame

from ship import Ship
from settings import Settings as game_settings
import functions

class ShipPanel():
    def __init__(self, coordinates):
        self.panel = pygame.Surface(game_settings.ship_panel_size)
        self.coordinates = coordinates
        self.width = game_settings.ship_panel_size[0]
        self.height = game_settings.ship_panel_size[1]
        self.visible = False
        self.ships = []
        self.ships_counter = [4, 3, 2, 1]
        self.counter_rects = []
        self.font = pygame.font.Font(None, 40)
        for i in range(1, 5):
            self.ships.append(Ship(i))
        margine = 70
        x = 0
        y = 0
        i = 0
        for ship in self.ships:
            ship.update_coordinates((x, y))
            text_sprite = self.font.render("x " + str(self.ships_counter[i]), True, pygame.Color("black"))
            rect = text_sprite.get_rect()
            rect.x = x + ship.cell_width * game_settings.cell_width + 10
            rect.y = y
            self.counter_rects.append(rect)
            x += ship.cell_width * game_settings.cell_width + margine
            i += 1
            if i == 3:
                y = game_settings.border_size
                x = 0

    def update_counters(self, ship_array):
        self.ships_counter = functions.count_ships(ship_array)

    def update(self, screen):
        if self.visible:
            self.panel.fill(game_settings.bg_color)
            for i in range(0, 4):
                text_sprite = self.font.render("x " + str(self.ships_counter[i]), True, pygame.Color("black"))
                self.panel.blit(text_sprite, self.counter_rects[i])
            functions.draw_ships(self.panel, self.ships)
            screen.blit(self.panel, self.coordinates)


    def set_visible(self, arg):
        self.visible = arg