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
        self.action = action
        self.font = pygame.font.Font(const.TEXT_FONT, const.TEXT_SIZE)
        self.surface = self.font.render(self.text, True, self.color)
        Actor.__init__(self, self.surface)
        self.rect = self.surface.get_rect(center=location)

    def update_text(self, text):
        self.text = text

    def update(self):
        self.surface = self.font.render(self.text, True, self.color)
        Actor.image = self.surface

    def draw(self, screen):
        render = screen.blit(self.surface, self.rect)
        return render;

    def on_click(self):
        self.action()
