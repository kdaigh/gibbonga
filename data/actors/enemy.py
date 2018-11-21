## @file enemy.py
#  Source file for enemy object
#
#  Project: Galaga Clone
#  Author: Py Five
#  Created: 10/17/18

import random
from .. import setup, constants, actor


## @class Enemy
#  @brief Implements Actor base class as Enemy object
class Enemy(actor.Actor):

    ## Constructor
    #  @param image, surface object with Enemy image
    def __init__(self, row, col):
        #actor.Actor.__init__(self, setup.IMAGES['enemy_spaceship'])
        actor.Actor.__init__(self, setup.IMAGES['enemy2'])
        self.rect.x = constants.ENEMY_WIDTH + (constants.ENEMY_WIDTH * col)
        self.rect.y = 100 + (constants.ENEMY_HEIGHT * row)
        self.x_dir = 1
        self.y_dir = 0
        self.speed = constants.ENEMY_SPEED
        self.drop = constants.ENEMY_DROP

    ## Function to update the enemy
    def update(self):
        self.rect[0] = self.rect[0] + (self.x_dir * self.speed)
        self.rect[1] = self.rect[1] + (self.y_dir * self.drop)

    # ## Constructor
    # #  @param image, surface object with Enemy image
    # def __init__(self):
    #     actor.Actor.__init__(self, setup.IMAGES['enemy_spaceship'])
    #     self.right = True
    #     self.down = True
    #     self.rect.y = constants.SCREENRECT.top
    #     self.rect.x = constants.SCREENRECT.left
    #     self.speed = random.randrange(2, 4)
    #     self.ychange = random.randrange(1,4)
    #     divide_list = [50, 60, 80]
    #     self.number = random.sample(divide_list, 1)
    #     self.count = 0
    #
    # ## Function to update the enemy
    # def update(self):
    #     self.count += 1
    #     if self.right == True:
    #         #if(self.rect.x == 614):
    #         if(self.rect.x == (constants.SCREENRECT.right - 30)):
    #             self.right = False
    #         self.rect.x += self.speed
    #     elif self.right == False:
    #         if(self.rect.x == 0):
    #             self.right = True
    #         self.rect.x -= self.speed
    #     if(self.down == False):
    #         self.rect.y -= self.ychange
    #         if(self.count%20 == 0):
    #             self.down = True
    #     elif(self.down == True):
    #         self.rect.y += self.ychange
    #         if(self.count%self.number[0] == 0):
    #             self.down = False
    #     self.rect = self.rect.clamp(constants.SCREENRECT)

    ## Checks for collisions
    #  @param actor, check collisions with this actor
    #  @returns bool, True if collision is detected; false, otherwise
    def collision_check(self, actor):
        return self.rect.colliderect(actor.rect)
