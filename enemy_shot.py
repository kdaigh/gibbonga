## @file shot.py
#  Source file for shot object
#
#  Project: Gallaga Clone
#  Author: Py Five
#  Created: 10/17/19

import pygame
from actor import Actor
import constants as const


## @class Shot
#  @brief Implements Actor base class as Shot object
class Enemy_shot(Actor):

    ## Constructor
    #  @param image, surface object with Shot image
    #  @param player, Player object that fired the shot
    def __init__(self, image, enemy):
        Actor.__init__(self, image)
        self.rect.centerx = enemy.rect.centerx
        self.rect.bottom = enemy.rect.bottom + 12

        #print (self.rect)


    # Updates the shot object
    def update(self):
        #self.rect[0] = self.rect[0] + self.rect.bottom
        while self.rect.bottom < 415:
            self.rect.bottom= self.rect.bottom + 10
            print (self.rect)
    ## Checks for collisions
    #  @param actor, check collisions with this actor
    #  @returns bool, True if collision is detected; false, otherwise
    def collision_check(self, actor):
        return self.rect.colliderect(actor.rect)
