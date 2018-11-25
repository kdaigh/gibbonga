## @file recover_health.py
#  Source file for health power-up
#
#  Project: Galaga Clone
#  Author: Py Five
#  Created: 11/05/18

import random
from .. import setup, constants, actor


## @class Recover_health
#  @brief Implements Actor base class as a Recover_health object
class Recover_health(actor.Actor):

    ## Constructor
    #  @param image, surface object with Player image
    def __init__(self):
        actor.Actor.__init__(self, setup.IMAGES['heart_power_up'])
        self.rect.x = random.randrange(15, 585)
        self.rect.y = constants.SCREENRECT.top

    ## Moves powerup down the screen
    #  @pre: Player object exists
    #  @param: direction, coordinates that represent desired move
    #  @post: icon location has been updated
    def update(self):
        self.rect.bottom = self.rect.bottom + 5
