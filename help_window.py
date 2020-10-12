import pygame
from pygame_menu.widgets import ScrollBar
import pygame_menu.locals as _locals

from settings import Settings as game_settings

class HelpWindow():
    def __init__(self):
        self.help_window = pygame.Surface(game_settings.help_window_size)
        self.size = game_settings.help_window_size
        self.width = game_settings.help_window_size[0]
        self.height = game_settings.help_window_size[1]
        self.scrollbar = ScrollBar(self.height,
                         (0, 1),
                         '',
                         _locals.ORIENTATION_VERTICAL,
                         2,
                         game_settings.field_color,
                         game_settings.scrollbar_size[1],
                         (253, 246, 220))
        self.scrollbar.set_shadow(color=(0, 0, 0),
                        position=_locals.POSITION_NORTHWEST,
                        offset=2)
        self.scrollbar.set_controls(False)
        self.scrollbar.set_position(self.width - game_settings.scrollbar_size[0], 0)
        self.text = ''
        self.default_text_coordinates = (10, 10)
        self.text_rects = []
        self.text_lines_surf = []
        self.add_log(game_settings.battleship_rules_text, False)
        self.counter = 0


    def update(self, screen, event):
        self.help_window.fill(game_settings.help_window_color)
        # self.update_scrollbar(screen, event)
        self.scrollbar.draw(self.help_window)
        self.draw_text(screen)
        trunc_world_orig = (0, self.scrollbar.get_value())
        trunc_world = self.size
        screen.blit(self.help_window, game_settings.help_window_coordinates, (trunc_world_orig, trunc_world))


    def update_scrollbar(self, screen, event):
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            event.pos = event.pos[0] - game_settings.help_window_coordinates[0], \
                        event.pos[1] - game_settings.help_window_coordinates[1]
        self.scrollbar.update([event])
        self.scrollbar.draw(self.help_window)

    def add_height(self, addend):
        new_scrollbar_max = self.scrollbar.get_maximum() + addend
        self.height = self.height+ addend
        self.help_window = pygame.transform.scale(self.help_window, (self.width, self.height))
        self.scrollbar.set_length(self.height)
        self.scrollbar.set_maximum(new_scrollbar_max)

    def add_log(self, text, game_log=True, turn_log = False):
        if turn_log:
            self.counter += 1
            text = str(self.counter) + '. ' + text
        text = self.process_text(text)
        self.add_text(text, game_log)

    def add_text(self, text, game_log):
        x, y = self.default_text_coordinates
        lines = text.splitlines()
        for line in lines:
            line_sprite = pygame.font.Font(None, game_settings.help_window_font_size).render(line, True,
                                                                               pygame.Color("black"))
            self.text_lines_surf.append(line_sprite)
            self.text_rects.append(line_sprite.get_rect())
            self.text_rects[0].x, self.text_rects[0].y = 0, 0
        for rect in self.text_rects:
            rect.y = y
            rect.x = x
            y += game_settings.help_window_font_size
            # self.text_rects.y = self.default_text_coordinates[1]
            if y >= self.height:
                self.add_height(game_settings.help_window_font_size)
        if game_log:
            self.scrollbar.set_value(self.scrollbar.get_maximum())

    def draw_text(self, screen):
        height = self.height
        for i in range(0, len(self.text_lines_surf)):
            self.help_window.blit(self.text_lines_surf[i], self.text_rects[i])



    def process_text(self, text):
        max_in_row = int(self.width/game_settings.help_window_font_size*2)
        counter = 0
        last_space = 0
        for i in range(0, len(text)):
            letter = text[i]
            if text[i] == '\n':
                counter = 0
            if counter >= max_in_row:
                text = text[0:last_space] + '\n' + text[last_space+1:]
                counter = 0
                i = last_space+1
            if text[i] == ' ':
                last_space = i
            counter += 1
        return text
