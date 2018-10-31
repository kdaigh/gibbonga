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
        #this is starting it from the left or from the right
        self.right = True
        self.down = True
        self.rect.y = const.SCREENRECT.top
        self.rect.x = const.SCREENRECT.left
        self.speed = random.randrange(5, 7)
        self.ychange = random.randrange(1,4)
        divide_list = [40, 50, 60]
        self.number = random.sample(divide_list, 1)
        self.count = 0
         # For now we are not letting enemies reload

    ## Function to update the enemy
    def update(self):
        self.count += 1
        if self.right == True:
            if(self.rect.x == 614):
                self.right = False
            self.rect.x += self.speed
        elif self.right == False:
            if(self.rect.x == 0):
                self.right = True
            self.rect.x -= self.speed
        if(self.down == False):
            self.rect.y -= self.ychange
            if(self.count%20 == 0):
                self.down = True
        elif(self.down == True):
            self.rect.y += self.ychange
            if(self.count%self.number[0] == 0):
                self.down = False
        self.rect = self.rect.clamp(const.SCREENRECT)

    ## Checks for collisions
    #  @param actor, check collisions with this actor
    #  @returns bool, True if collision is detected; false, otherwise
    def collision_check(self, actor):
        return self.rect.colliderect(actor.rect)
