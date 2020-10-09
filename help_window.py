import pygame
from pygame_menu.widgets import ScrollBar

from settings import Settings as game_settings


class HelpWindow(pygame.Surface):
    def __init__(self):
        pygame.Surface.__init__(self, game_settings.help_window_size)
        # self.scrollbar =ScrollBar(game_settings.help_window_size[0]-game_settings.scrollbar_width,
        #                           (50, world.get_width() - scr_size[0] + thick_v),
        #                           slider_pad=2,
        #                           page_ctrl_thick=thick_h,
        #                           onchange=h_changed)
        # )

    def update(self):
        self.fill(game_settings.help_window_color)