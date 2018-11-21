## @file recover_health.py
#  Source file for health power-up
#
#  Project: Galaga Clone
#  Author: Py Five
#  Created: 11/05/18

from components.actor import Actor
import setup
import random
import constants as const


## @class Recover_health
#  @brief Implements Actor base class as a health power-up
class Recover_health(Actor):

    ## Constructor
    #  @param image, surface object with Player image
    def __init__(self):
        Actor.__init__(self, setup.IMAGES['hearts_1'])
        self.rect.x = random.randrange(15, 585)
        self.rect.y = const.SCREENRECT.top

    ## Moves powerup down the screen
    #  @pre: Player object exists
    #  @param: direction, coordinates that represent desired move
    #  @post: icon location has been updated
    def update(self):
        self.rect.bottom = self.rect.bottom + 5
