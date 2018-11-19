## @file text.py
#  Source file for Text base class
#
#  Project: Gallaga Clone
#  Author: Py Five
#  Created: 11/18/19

# TBD: Import statements
import pygame
import constants as const

## @class Text
#  @brief Defines Text base class
class Text:

    ## TBD: Constructor
    def __init__(self, text, color, location, action):
        self.text = text
        self.color = color
        self.action = action
        self.font = pygame.font.Font(const.TEXT_FONT, const.TEXT_SIZE)
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(center=location)

    def draw(self, screen):

        # TBD: Initiate hover function
        # self.hover()

        render = screen.blit(self.surface, self.rect)
        return render;

    ## TBD hover functionality
    def hover(self):
        pass

    # Add in game
    # def click():
    #     pos = pygame.mouse.get_pos()
    #     for button in buttons:
    #         if buton.rect.collidepoint(pos):
    #             button.on_click()
    def on_click(self):
        self.action()
