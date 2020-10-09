import random
from settings import Settings as game_settings
import functions as func
import time

class Enemy():
    def __init__(self):
        self.last_hit = self.correct_hit = None
        self.sides = {'right': (0, 1),
                                        'left': (0, -1),
                                        'top': (-1, 0),
                                        'bottom': (1, 0)}
        self.temp_sides = self.sides.copy()
        self.horizontal_ship = False
        self.vertical_ship = False
        self.missfire = False
        self.first_blood = False

    def play(self):
        side = None
        i = j = -1
        if self.last_hit and self.temp_sides:
            while True:
                side = random.choice(list(self.temp_sides.keys()))
                correctors = self.sides.get(side)
                next_shoot = self.last_hit + correctors
                i = next_shoot[0] + correctors[0]
                j = next_shoot[1] + correctors[1]
                if func.correct_coordinates(i, j):
                    break
                else:
                    del self.temp_sides[side]
        else:
            i = random.randint(0, game_settings.cells_in_row_number - 1)
            j = random.randint(0, game_settings.cells_in_row_number - 1)
        return i, j, side

    def hited(self, i, j):
        self.last_hit = (i, j)

    def cancel_hited(self):
        self.last_hit = None

    def turn(self, player_field, player_ship_array):
        self.missfire = False
        i, j, side = self.play()
        shoot_result = func.shoot((i, j), player_field, player_ship_array)

        if shoot_result:
            if shoot_result not in ('alredy injured', 'already missfire'):
                time.sleep(0.5)
            if shoot_result == 'injured':
                self.hited(i, j)
                if not self.first_blood:
                    self.first_blood = True
                    self.correct_hit = self.last_hit
            elif shoot_result == 'killed':
                self.last_hit = None
                self.correct_hit = None
                self.first_blood = False
                self.temp_sides = self.sides.copy()
            elif shoot_result == 'missfire':
                self.missfire = True
                if self.last_hit:
                    del self.temp_sides[side]
            elif shoot_result == 'already injured' and len(self.temp_sides) == 1:
                self.last_hit = self.correct_hit
            elif shoot_result == 'already missfire' and self.first_blood:
                del self.temp_sides[side]

        # else:
        #     if self.last_hit:
        #         self.last_hit = self.correct_hit
        print('\nenemy play')
        print('last_hit = ' + str(self.last_hit))
        print('correct_hit = ' + str(self.correct_hit))
        print('side = ' + str(side))
        print('shoot result = ' +str(shoot_result))
        print(self.temp_sides)
