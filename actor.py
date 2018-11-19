## @file actor.py
#  Source file for actor base class
#
#  Project: Gallaga Clone
#  Author: Py Five
#  Created: 10/17/19

import pygame
from pygame.locals import *


## @class Actor
#  @brief Abstract base class for game actors
class Actor:

    ## Constructor
    #  @param image, surface object with Actor image
    def __init__(self, image):
        self.image = image
        self.rect = image.get_rect()

    ## Abstract method; Updates actor in frame
    def update(self):
        pass

    ## Draws the actor into the screen
    #  @param: screen, screen which actor will be drawn onto
    #  @returns: render, new render of actor
    def draw(self, screen):
        render = screen.blit(self.image, self.rect)
        return render;

    ## Removes the actor from the screen
    #  @param: screen, screen which actor will be erased from
    #  @param: background, background that will be drawn over actor
    #  @returns: render, new render of actor
    def erase(self, screen, background):
        render = screen.blit(background, self.rect, self.rect)
        return render;


