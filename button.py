import pygame

from settings import Settings as gs

class Button():
    def __init__(self):
        self.text = pygame.font.Font(None, 40).render("Start", True, gs.bg_color)
        self.text_rect = self.text.get_rect(center = (gs.start_button_x + gs.start_button_width/2,
                                                      gs.start_button_y + gs.start_button_height/2))
        self.rect = pygame.Rect(gs.start_button_coordinates, gs.start_button_size)
        self.clickable = True



    def update(self, screen):
        if self.clickable:
            pygame.draw.rect(screen, gs.start_button_color, self.rect)
        else:
            pygame.draw.rect(screen, pygame.Color("gray"), self.rect)
        screen.blit(self.text, self.text_rect)

    def is_clickable(self):
        return self.clickable

    def make_cklickable(self):
        self.clickable = True

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)

    def onclick(self):
        self.clickable = False
        pass



