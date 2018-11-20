## @file shot.py
#  Source file for shot object
#
#  Project: Galaga Clone
#  Author: Py Five
#  Created: 10/17/18

from actor import Actor
import setup


## @class Shot
#  @brief Implements Actor base class as Shot object
class Enemy_shot(Actor):

    ## Constructor
    #  @param image, surface object with Shot image
    #  @param player, Player object that fired the shot
    def __init__(self, enemy):
        Actor.__init__(self, setup.IMAGES['missile2'])
        self.rect.centerx = enemy.rect.centerx
        self.rect.bottom = enemy.rect.bottom + 12

    # Updates the shot object
    def update(self):
        self.rect.bottom = self.rect.bottom + 10


