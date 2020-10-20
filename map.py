import pygame

import config


class Map(pygame.Surface):
    def __init__(self, coordinates):
        pygame.Surface.__init__(self, config.field_size)
        self.coordinates = coordinates
        self.letters = []
        self.letters_rects = []
        self.letters_x = coordinates[0]
        self.letters_y = coordinates[1] - config.cell_width
        for i in range(0, len(config.letters)):
            letter_sprite = pygame.font.Font(None, 30).render(config.letters[i], True, pygame.Color("black"))
            self.letters.append(letter_sprite)
            self.letters_rects.append(letter_sprite.get_rect(
                center=(self.letters_x + config.cell_width / 2 + i * config.cell_width,
                        self.letters_y + config.cell_width / 2)))

        self.numbers = []
        self.numbers_rects = []
        self.numbers_x = coordinates[0] - config.cell_width
        self.numbers_y = coordinates[1]
        for i in range(0, len(config.numbers)):
            number_sprite = pygame.font.Font(None, 30).render(config.numbers[i], True, pygame.Color("black"))
            self.numbers.append(number_sprite)
            self.numbers_rects.append(number_sprite.get_rect(
                center=(self.numbers_x + config.cell_width / 2,
                        self.numbers_y + config.cell_width / 2 + i * config.cell_width)))

    def update(self, screen):
        self.fill(config.field_color)
        # Draw borders and grid
        for i in range(0, config.field_width, int(config.field_width / 10)):
            pygame.draw.line(self, config.line_color, (i, 0), (i, config.field_width))  # vertical
            pygame.draw.line(self, config.line_color, (0, i), (config.field_width, i))  # horizontal
        for i in range(0, config.cells_in_row_number):
            screen.blit(self.letters[i], self.letters_rects[i])
            screen.blit(self.numbers[i], self.numbers_rects[i])
