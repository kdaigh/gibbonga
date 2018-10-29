## @file enemy.py
#  Source file for enemy object
#
#  Project: Gallaga Clone
#  Author: Py Five
#  Created: 10/17/19

from actor import Actor
import random
import constants as const


## @class Enemy
#  @brief Implements Actor base class as Enemy object
class Enemy(Actor):

    ## Constructor
    #  @param image, surface object with Enemy image
    def __init__(self, image):
        Actor.__init__(self, image)
        self.direction = random.randrange(-1, 2) * const.ENEMY_SPEED
        if self.direction > 0:
            self.rect.left = const.SCREENRECT.left
        else:
            self.rect.right = const.SCREENRECT.right
         # For now we are not letting enemies reload

    ## Function to update the enemy
    def update(self):
        self.rect[0] = self.rect[0] + self.direction
        if not const.SCREENRECT.contains(self.rect):
            self.direction = - self.direction
            self.rect.top = self.rect.bottom + 50
            self.rect = self.rect.clamp(const.SCREENRECT)

    ## Checks for collisions
    #  @param actor, check collisions with this actor
    #  @returns bool, True if collision is detected; false, otherwise
    def collision_check(self, actor):
        return self.rect.colliderect(actor.rect)
