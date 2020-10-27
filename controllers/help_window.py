import pygame
import pygame_menu.locals as _locals
from pygame_menu.widgets import ScrollBar

import config


class HelpWindow:
    def __init__(self):
        self.__surface = pygame.Surface(config.help_window_size)
        self.size = config.help_window_size
        self.width = config.help_window_size[0]
        self.height = config.help_window_size[1]
        self.font = pygame.font.Font(None, config.help_window_font_size)
        self.__scrollbar = ScrollBar(self.height,
                                     (0, 1),
                                     '',
                                     _locals.ORIENTATION_VERTICAL,
                                     2,
                                     config.field_color,
                                     config.scrollbar_size[1],
                                     (253, 246, 220))
        self.__scrollbar.set_shadow(color=(0, 0, 0),
                                    position=_locals.POSITION_NORTHWEST,
                                    offset=2)
        self.__scrollbar.set_controls(False)
        self.__scrollbar.set_position(self.width - config.scrollbar_size[0], 0)
        self.text = ''
        self.default_text_coordinates = (10, 10)
        self.text_rects = []
        self.text_lines_surf = []
        self.add_log(config.battleship_rules_text, False)
        self.counter = 0

    def update(self, screen):
        self.__surface.fill(config.help_window_color)
        # self.update_scrollbar(screen, event)
        self.__scrollbar.draw(self.__surface)
        self.draw_text()
        trunc_world_orig = (0, self.__scrollbar.get_value())
        trunc_world = self.size
        screen.blit(self.__surface, config.help_window_coordinates, (trunc_world_orig, trunc_world))

    def update_scrollbar(self, event):
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            event.pos = event.pos[0] - config.help_window_coordinates[0], \
                        event.pos[1] - config.help_window_coordinates[1]
        self.__scrollbar.update([event])
        self.__scrollbar.draw(self.__surface)

    def change_height(self, new_height):
        new_scrollbar_max = self.__scrollbar.get_maximum() + (new_height - self.height)
        self.height = new_height
        self.__surface = pygame.transform.scale(self.__surface, (self.width, self.height))
        self.__scrollbar.set_length(self.height)
        self.__scrollbar.set_maximum(new_scrollbar_max)

    def add_log(self, text, game_log=True, turn_log=False):
        if turn_log:
            self.counter += 1
            text = str(self.counter) + '. ' + text
        text = self.process_text(text)
        self.add_text(text, game_log)

    def add_text(self, text, game_log):
        x, y = self.default_text_coordinates
        lines = text.splitlines()
        for line in lines:
            line_sprite = self.font.render(line, True, pygame.Color("black"))
            self.text_lines_surf.append(line_sprite)
            self.text_rects.append(line_sprite.get_rect())
            self.text_rects[0].x, self.text_rects[0].y = 0, 0
        for rect in self.text_rects:
            rect.y = y
            rect.x = x
            y += config.help_window_font_size
            # self.text_rects.y = self.default_text_coordinates[1]
            if y >= self.height:
                self.change_height(self.height + config.help_window_font_size)
        if game_log:
            self.__scrollbar.set_value(self.__scrollbar.get_maximum())

    def draw_text(self):
        for i in range(0, len(self.text_lines_surf)):
            self.__surface.blit(self.text_lines_surf[i], self.text_rects[i])

    def process_text(self, text):
        max_in_row = int(self.width / config.help_window_font_size * 2)
        counter = 0
        last_space = 0
        for i in range(0, len(text)):
            if text[i] == '\n':
                counter = 0
            if counter >= max_in_row:
                text = text[0:last_space] + '\n' + text[last_space + 1:]
                counter = 0
                i = last_space + 1
            if text[i] == ' ':
                last_space = i
            counter += 1
        return text

    def return_to_default(self):
        self.text_rects.clear()
        self.text_lines_surf.clear()
        self.add_log(config.battleship_rules_text, False)
        self.counter = 0
        self.change_height(config.help_window_size[1])
