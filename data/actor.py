## @file actor.py
#  Source file for actor base class
#
#  Project: Galaga Clone
#  Author: Py Five
#  Created: 10/17/18


## @class Actor
#  @brief Abstract base class for game actors
class Actor:

    ## Constructor
    #  @param image, surface object with Actor image
    def __init__(self, image):
        self.image = image
        self.rect = image.get_rect()
        self.alive = True

    ## Abstract method; Updates actor in frame
    def update(self):
        pass

    ## Draws the actor into the screen
    #  @param screen, screen which actor will be drawn onto
    #  @returns render, new render of actor
    def draw(self, screen):
        render = screen.blit(self.image, self.rect)
        return render;

    ## Checks for collisions and sets "alive" variable if hit
    #  @param actor, check collisions with this actor
    #  @post Alive variable has been set accordinly
    #  @returns bool, True if collision is detected; false, otherwise
    def collide_with(self, actor):
        if self.rect.colliderect(actor.rect):
            self.alive = False
            return True
        else:
            return False

    ## Removes the actor from the screen
    #  @param screen, screen which actor will be erased from
    #  @param background, background that will be drawn over actor
    #  @returns render, new render of actor
    def erase(self, screen, background):
        render = screen.blit(background, self.rect, self.rect)
        return render;
