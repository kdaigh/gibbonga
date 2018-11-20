## @file player.py
#  Source file for player object
#
#  Project: Galaga Clone
#  Author: Py Five
#  Created: 10/17/18

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

    ## Reacts to player being hit by a threat
    #  @post Hit sound played and health decremented
    def hit(self):
        setup.SOUNDS['hit'].play()
        self.health -= 1
        if self.health == 0:
            self.alive = False

    ## Reacts to player picking up recovery health
    #  @post Power-up sound played and health incremented
    def recover(self):
        setup.SOUNDS['power_up2'].play()
        self.health += 1
