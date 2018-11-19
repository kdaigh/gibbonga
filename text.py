## @file text.py
#  Source file for Text base class
#
#  Project: Gallaga Clone
#  Author: Py Five
#  Created: 11/18/19

# TBD: Import statements
import pygame
import constants as const
from actor import Actor

## @class Text
#  @brief Defines Text base class
class Text(Actor):

    ## TBD: Constructor
    def __init__(self, text, color, location, action):
        self.text = text
        self.color = color
        self.location = location
        self.action = action
        self.font = pygame.font.Font(const.TEXT_FONT, const.TEXT_SIZE)
        image = self.font.render(self.text, True, self.color)
        Actor.__init__(self, image)
        self.rect = self.image.get_rect(center=self.location)

    def update_text(self, text):
        self.text = text
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect(center=self.location)

    # def draw(self, screen):
    #     self.surface = self.font.render(self.text, True, self.color)
    #     render = screen.blit(self.surface, self.rect)
    #     return render;

    def on_click(self):
        self.action()
