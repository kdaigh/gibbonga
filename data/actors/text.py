## @file text.py
#  Source file for Text base class
#
#  Project: Galaga Clone
#  Author: Py Five
#  Created: 11/18/18

import pygame
from .. import constants, actor

## @class Text
#  @brief Defines Text base class
class Text(actor.Actor):

    ## Constructor
    #  @param text, text to be printed on screen
    #  @param color, color of text
    #  @param location, coordinates for text
    #  @param action, function to execute on click [OPTIONAL]
    def __init__(self, text, color, location, action=lambda x: None):
        self.text = text
        self.color = color
        self.location = location
        self.action = action
        self.font = pygame.font.Font(constants.GAME_FONT, constants.TEXT_SIZE)
        image = self.font.render(self.text, True, self.color)
        actor.Actor.__init__(self, image)
        self.rect = self.image.get_rect(center=self.location)

    ## Updates the text, image, and coordinates of the text object
    #  @param text, text to be printed on screen
    def update_text(self, text):
        self.text = text
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(center=self.location)

    ## Executes on click function [if provided]
    #  @pre A function has been provided
    def on_click(self):
        self.action()
