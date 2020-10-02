import pygame
from settings import Settings as game_settings


class Field(pygame.Surface):
    def __init__(self, coordinates):
        pygame.Surface.__init__(self, game_settings.field_size)
        self.coordinates = coordinates
        self.letters = []
        self.letters_rects = []
        self.letters_x = coordinates[0]
        self.letters_y = coordinates[1] - game_settings.cell_width
        for i in range(0, len(game_settings.letters)):
            letter_sprite = pygame.font.Font(None, 30).render(game_settings.letters[i], True, pygame.Color("black"))
            self.letters.append(letter_sprite)
            self.letters_rects.append(letter_sprite.get_rect(
                center = (self.letters_x + game_settings.cell_width/2 + i*game_settings.cell_width,
                          self.letters_y + game_settings.cell_width/2)))

        self.numbers = []
        self.numbers_rects = []
        self.numbers_x = coordinates[0] - game_settings.cell_width
        self.numbers_y = coordinates[1]
        for i in range(0, len(game_settings.numbers)):
            number_sprite = pygame.font.Font(None, 30).render(game_settings.numbers[i], True, pygame.Color("black"))
            self.numbers.append(number_sprite)
            self.numbers_rects.append(number_sprite.get_rect(
                center = (self.numbers_x + game_settings.cell_width/2,
                          self.numbers_y + game_settings.cell_width/2 + i*game_settings.cell_width)))


    def update(self, screen):
        self.fill(game_settings.field_color)
        #Draw borders and grid
        for i in range(0, game_settings.field_width, int(game_settings.field_width/10)):
            pygame.draw.line(self, game_settings.line_color, (i, 0), (i, game_settings.field_width)) #vertical
            pygame.draw.line(self, game_settings.line_color, (0, i), (game_settings.field_width, i))  # horizontal
        for i in range(0, game_settings.cells_in_row_number):
            screen.blit(self.letters[i], self.letters_rects[i])
            screen.blit(self.numbers[i], self.numbers_rects[i])