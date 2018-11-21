## @file health.py
#  Source file for health object
#
#  Project: Galaga Clone
#  Author: Py Five
#  Created: 10/24/18

from actor import Actor
import constants as const
import setup

## @class Health
#  @brief Implements Actor base class as Health object
class Health(Actor):

    ## Constructor
    #  @param image, surface object with Health image
    #  @param player, Player object that will be linked with health
    def __init__(self, player):
        Actor.__init__(self, setup.IMAGES['hearts_3'])
        self.health = 3
        self.player = player
        self.rect.left = const.SCREENRECT.left
        self.rect.bottom = const.SCREENRECT.bottom

    def increase(self):
        if self.health < 3:
            self.health += 1

    def decrease(self):
        if self.health > 0:
            self.health -= 1

    def update(self):
        if self.health <= 0:
            self.image = setup.IMAGES['hearts_0']
        elif self.health == 1:
            self.image = setup.IMAGES['hearts_1']
        elif self.health == 2:
            self.image = setup.IMAGES['hearts_2']
        elif self.health >= 3:
            self.image = setup.IMAGES['hearts_3']
