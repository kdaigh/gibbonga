## @file level.py
#  Source file for levels
#
#  Project: Galaga Clone
#  Author: Py Five
#  Created: 11/21/18

import pygame
from . import constants, setup
from .actors.enemy import Enemy


## @class Level
#  @brief Manages the game levels and corresponding enemies
class Level:

    ## Constructor
    def __init__(self):
        self.level = 0
        self.ENEMY_ROWS = 0
        self.ENEMIES_PER_ROW = 0
        self.TOTAL_ENEMIES = 0
        self.ENEMY_SPEED = 0
        self.ENEMY_DROP_DIST = 0
        self.direction = 1
        self.drop = 0

    ## Generates a fleet of enemies for the level
    #  @returns enemies, Enemy array for game
    def generate_enemies(self):
        enemies = []
        for row_number in range(self.ENEMY_ROWS):
            for enemy_number in range(self.ENEMIES_PER_ROW):
                enemy = Enemy()
                enemy.spawn_at(row_number, enemy_number)
                enemy.image = setup.IMAGES['enemy2']
                enemies.append(enemy)
        return enemies

    ## Updates enemy fleet movements
    #  @param enemies, Enemy array from game
    def update(self, enemies):
        for enemy in enemies:
            if enemy.rect.left <= constants.SCREENRECT.left:
                self.direction = 1
                self.drop = 1
            elif enemy.rect.right >= constants.SCREENRECT.right:
                self.direction = -1
                self.drop = 1
            else:
                self.drop = 0

        for enemy in enemies:
            enemy.x_move = self.ENEMY_SPEED * self.direction
            enemy.y_move = self.ENEMY_DROP_DIST * self.drop

    ## Increments level counter and updates game properties for level
    def next_level(self):
        if self.level > 0:
            setup.SOUNDS['sfx_coin_cluster3'].play()
            pygame.time.delay(500)
        self.level += 1
        self.ENEMY_ROWS = constants.ENEMY_ROWS[self.level]
        self.ENEMIES_PER_ROW = constants.ENEMIES_PER_ROW[self.level]
        self.TOTAL_ENEMIES = constants.TOTAL_ENEMIES[self.level]
        self.ENEMY_SPEED = constants.ENEMY_SPEED[self.level]
        self.ENEMY_DROP_DIST = constants.ENEMY_DROP_DIST[self.level]

    ## Checks whether player has successfully completed current level
    #  @param score, current score of the game
    #  @returns Bool, True if the level has been won; false, otherwise
    def pass_level(self, score):
        if score >= self.TOTAL_ENEMIES:
            return True
        return False

    ## Checks whether player has successfully completed all levels
    #  @param score, current score of the game
    #  @returns Bool, True if the game has been won; false, otherwise
    def game_win(self, score):
        if self.level == constants.TOTAL_LEVELS and self.pass_level(score):
            return True
        return False
