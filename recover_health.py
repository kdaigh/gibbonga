from actor import Actor
import setup
import random
import constants as const

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
        self.rect.bottom = self.rect.bottom + 10

    ## Checks for player collecting a powerup
    #  @param actor, check collisions with this actor
    #  @returns bool, True if collision is detected; false, otherwise
    def pickup(self, actor):
        return self.rect.colliderect(actor.rect)
