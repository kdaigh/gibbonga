## @file enemy_shot.py
#  Source file for enemy shot object
#
#  Project: Galaga Clone
#  Author: Py Five
#  Created: 10/17/18

from .. import setup, actor


## @class Shot
#  @brief Implements Actor base class as Shot object
class Enemy_shot(actor.Actor):

    ## Constructor
    #  @param image, surface object with Shot image
    #  @param player, Player object that fired the shot
    def __init__(self, enemy):
        actor.Actor.__init__(self, setup.IMAGES['missile2'])
        self.rect.centerx = enemy.rect.centerx
        self.rect.bottom = enemy.rect.bottom + 12

    # Updates the shot object
    def update(self):
        self.rect.bottom = self.rect.bottom + 10


