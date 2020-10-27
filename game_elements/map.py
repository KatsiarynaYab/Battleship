import pygame

import config


class Map(pygame.Surface):
    def __init__(self, coordinates):
        pygame.Surface.__init__(self, config.field_size)
        self.coordinates = coordinates
        self.__letters = []
        self.__letters_rects = []
        self._letters_x = coordinates[0]
        self._letters_y = coordinates[1] - config.cell_width
        for i in range(0, len(config.letters)):
            letter_sprite = pygame.font.Font(None, 30).render(config.letters[i], True, pygame.Color("black"))
            self.__letters.append(letter_sprite)
            self.__letters_rects.append(letter_sprite.get_rect(
                center=(self._letters_x + config.cell_width / 2 + i * config.cell_width,
                        self._letters_y + config.cell_width / 2)))

        self.__numbers = []
        self.__numbers_rects = []
        self.numbers_x = coordinates[0] - config.cell_width
        self.numbers_y = coordinates[1]
        for i in range(0, len(config.numbers)):
            number_sprite = pygame.font.Font(None, 30).render(config.numbers[i], True, pygame.Color("black"))
            self.__numbers.append(number_sprite)
            self.__numbers_rects.append(number_sprite.get_rect(
                center=(self.numbers_x + config.cell_width / 2,
                        self.numbers_y + config.cell_width / 2 + i * config.cell_width)))

    def update(self, screen):
        self.fill(config.field_color)
        # Draw borders and grid
        for i in range(0, config.field_width, int(config.field_width / 10)):
            pygame.draw.line(self, config.line_color, (i, 0), (i, config.field_width))  # vertical
            pygame.draw.line(self, config.line_color, (0, i), (config.field_width, i))  # horizontal
        for i in range(0, config.cells_in_row_number):
            screen.blit(self.__letters[i], self.__letters_rects[i])
            screen.blit(self.__numbers[i], self.__numbers_rects[i])
