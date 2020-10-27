import random
import time

import config
from functions import game_functions as func


class Enemy:
    def __init__(self):
        self.__last_hit = self.__correct_hit = None
        self.__sides = {'right': (0, 1),
                        'left': (0, -1),
                        'top': (-1, 0),
                        'bottom': (1, 0)}
        self.__temp_sides = self.__sides.copy()
        self.__horizontal_ship = False
        self.__vertical_ship = False
        self.__first_blood = False
        self.missfire = False

    def play(self):
        side = None
        if self.__last_hit and self.__temp_sides:
            while True:
                side = random.choice(list(self.__temp_sides.keys()))
                correctors = self.__sides.get(side)
                next_shoot = self.__last_hit + correctors
                i = next_shoot[0] + correctors[0]
                j = next_shoot[1] + correctors[1]
                if func.correct_coordinates(i, j):
                    break
                else:
                    del self.__temp_sides[side]
        else:
            i = random.randint(0, config.cells_in_row_number - 1)
            j = random.randint(0, config.cells_in_row_number - 1)
        return i, j, side

    def hited(self, i, j):
        self.__last_hit = (i, j)

    def cancel_hited(self):
        self.__last_hit = None

    def turn(self, player_field, player_ship_array, help_window):
        self.missfire = False
        i, j, side = self.play()
        shoot_result = func.shoot((i, j), player_field, player_ship_array)
        if shoot_result:
            if shoot_result not in ('already hit', 'already missfire'):
                time.sleep(0.5)
                letter, number = func.ij_to_game_coordinates(i, j)
                help_window.add_log(f"enemy choose {letter}{number}, {shoot_result}", turn_log=True)
            if shoot_result == 'hit':
                self.hited(i, j)
                if not self.__first_blood:
                    self.__first_blood = True
                    self.__correct_hit = self.__last_hit
            elif shoot_result == 'killed':
                self.__last_hit = None
                self.__correct_hit = None
                self.__first_blood = False
                self.__temp_sides = self.__sides.copy()
            elif shoot_result == 'missfire':
                self.missfire = True
                if self.__last_hit:
                    del self.__temp_sides[side]
            elif shoot_result == 'already hit' and len(self.__temp_sides) == 1:
                self.__last_hit = self.__correct_hit
            elif shoot_result == 'already missfire' and self.__first_blood:
                del self.__temp_sides[side]
