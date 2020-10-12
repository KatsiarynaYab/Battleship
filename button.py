import pygame

from settings import Settings as gs
from abc import ABC

class Button():
    def __init__(self, text, font_size, x, y, width, height, text_color):
        self.text = pygame.font.Font(None, font_size).render(text, True, text_color)
        self.text_rect = self.text.get_rect(center = (x + width/2, y + height/2))
        self.rect = pygame.Rect((x, y), (width, height))
        self.clickable = True
        self.visible = True

    def update(self, screen):
        pass

    def set_coordinates(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_visible(self, arg):
        self.visible = arg

    def set_clickable(self, arg):
        self.clickable = arg

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)





class StartButton(Button):
    def __init__(self):
        Button.__init__(self, "Start", 40, gs.start_button_x, gs.start_button_y,
                        gs.start_button_width, gs.start_button_height, gs.bg_color)

    def update(self, screen):
        if self.clickable:
            pygame.draw.rect(screen, gs.start_button_color, self.rect)
        else:
            pygame.draw.rect(screen, pygame.Color("gray"), self.rect)
        screen.blit(self.text, self.text_rect)

class RandomizeButton(Button):
    def __init__(self):
        Button.__init__(self, "Randomize field", 30, gs.random_button_x, gs.random_button_y,
                        gs.random_button_width, gs.random_button_height, gs.bg_color)

    def update(self, screen):
        pygame.draw.rect(screen, gs.random_button_color, self.rect)
        screen.blit(self.text, self.text_rect)

class YesNoButton(Button):
    def __init__(self, text, x, y):
        Button.__init__(self, text, 20, x, y, 50, gs.random_button_height, gs.bg_color)

    def update(self, screen):
        pygame.draw.rect(screen, gs.random_button_color, self.rect)
        screen.blit(self.text, self.text_rect)