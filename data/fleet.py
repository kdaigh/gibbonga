## @file fleet.py
#  Source file for fleet
#
#  Project: Galaga Clone
#  Author: Py Five
#  Created: 11/21/18

import random
from . import constants
from .actors.enemy import Enemy

## @class Fleet
#  @brief TBD
class Fleet:

    def __init__(self, rows, enemies_per_row):
        self.rows = rows
        self.enemies_per_row = enemies_per_row
        self.x_dir = 1
        self.y_dir = 0

    def generate_fleet(self):
        fleet = []
        for row_number in range(self.rows):
            for enemy_number in range(self.enemies_per_row):
                enemy = Enemy(row_number, enemy_number)
                fleet.append(enemy)
        return fleet

    def move_fleet(self, enemies):
        self.y_dir = 0
        for enemy in enemies:
            if enemy.rect.left <= constants.SCREENRECT.left:
                self.x_dir = 1
                self.y_dir = 1
                break
            elif enemy.rect.right >= constants.SCREENRECT.right:
                self.x_dir = -1
                self.y_dir = 1
                break

        for enemy in enemies:
            enemy.x_dir = self.x_dir
            enemy.y_dir = self.y_dir
