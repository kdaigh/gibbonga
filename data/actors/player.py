## @file player.py
#  Source file for player object
#
#  Project: Galaga Clone
#  Author: Py Five
#  Created: 10/17/18

from .. import setup, constants, actor


## @class Player
#  @brief Implements Actor base class as Player object
class Player(actor.Actor):

    ## Constructor
    #  @param image, surface object with Player image
    def __init__(self):
        actor.Actor.__init__(self, setup.IMAGES['starship'])
        self.alive = True
        self.health = 3
        self.reloading = False
        self.rect.centerx = constants.SCREENRECT.centerx
        self.rect.bottom = constants.SCREENRECT.bottom

    ## Moves player in a specific direction
    #  @pre Player object exists
    #  @param direction, coordinates that represent desired move
    #  @post Player location has been updated
    def move(self, direction):
        self.rect = self.rect.move(direction * constants.PLAYER_SPEED, 0).clamp(constants.SCREENRECT)

    ## Reacts to player being hit by a threat
    #  @post Hit sound played and health decremented
    def hit(self):
        if self.health > 0:
            setup.SOUNDS['hit'].play()
            self.health -= 1
            print (self.health)
        if self.health == 0:
            self.alive = False

    ## Reacts to player picking up recovery health
    #  @post Power-up sound played and health incremented
    def recover(self):
        if self.health < 3:
            setup.SOUNDS['power_up2'].play()
            self.health += 1
            print(self.health)
