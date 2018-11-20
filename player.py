## @file player.py
#  Source file for player object
#
#  Project: Gallaga Clone
#  Author: Py Five
#  Created: 10/17/19

from actor import Actor
import constants as const
import setup


## @class Player
#  @brief Implements Actor base class as Player object
class Player(Actor):

    ## Constructor
    #  @param image, surface object with Player image
    def __init__(self):
        Actor.__init__(self, setup.IMAGES['starship'])
        self.alive = True
        self.health = 3
        self.reloading = False
        self.rect.centerx = const.SCREENRECT.centerx
        self.rect.bottom = const.SCREENRECT.bottom

    ## Moves player in a specific direction
    #  @pre Player object exists
    #  @param direction, coordinates that represent desired move
    #  @post Player location has been updated
    def move(self, direction):
        self.rect = self.rect.move(direction * const.PLAYER_SPEED, 0).clamp(const.SCREENRECT)

    def hit(self):
        self.health -= 1
        if self.health == 0:
            self.alive = False

    def recover(self):
        self.health += 1
