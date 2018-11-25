## @file enemy.py
#  Source file for enemy object
#
#  Project: Galaga Clone
#  Author: Py Five
#  Created: 10/17/18

from .. import setup, constants, actor


## @class Enemy
#  @brief Implements Actor base class as Enemy object
class Enemy(actor.Actor):

    ## Constructor
    #  @param image, surface object with Enemy image
    def __init__(self):
        actor.Actor.__init__(self, setup.IMAGES['enemy4'])
        self.rect.x = constants.SCREENRECT.left
        self.rect.y = constants.SCREENRECT.top
        self.x_dir = 1
        self.y_dir = 0

    ## Places enemy at certain location in fleet
    #  @param enemy_rows, Number of rows
    #  @param enemies_per_row, Number of enemies per row
    def spawn_at(self, enemy_rows, enemies_per_row):
        self.rect.x = constants.ENEMY_WIDTH + (constants.ENEMY_WIDTH * enemies_per_row)
        self.rect.y = 100 + (constants.ENEMY_HEIGHT * enemy_rows)

    ## Function to move the enemy
    def update(self):
        self.rect.x = self.rect[0] + self.x_move
        self.rect.y = self.rect[1] + self.y_move

    ## Function to set the alive status of an enemy
    #  @post Variable alive set to False
    def die(self):
        self.alive = False
