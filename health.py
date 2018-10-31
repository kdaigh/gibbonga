## @file shot.py
#  Source file for shot object
#
#  Project: Gallaga Clone
#  Author: Py Five
#  Created: 10/24/19

import pygame
from actor import Actor
from player import Player

## @class Health
#  @brief Implements Actor base class as Health object
class Health(Actor):

    ## Constructor
    #  @param image, surface object with Shot image
    #  @param player, Player object that fired the shot
    def __init__(self, image, player):
        Actor.__init__(self, image)
        self.rect.centerx = player.rect.centerx
        self.rect.bottom = player.rect.bottom + 5
