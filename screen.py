## @file screen.py
#  Source file for screen base class
#
#  Project: Gallaga Clone
#  Author: Py Five
#  Created: 11/18/19

# TBD: Import statements
import pygame
import constants as const
from text import Text
import sys

## @class Screen
#  @brief Defines Screen base class
class Screen:

    ## TBD: Constructor
    def __init__(self):
        self.exit = False
        self.options = []
        self.texts = []

    def load_screen(self):

        #while not self.exit:
            screen = pygame.display.set_mode(const.SCREENRECT.size, 0)
            screen.fill((0, 0, 0))
            pygame.display.update()
            start_game = Text("START GAME", const.WHITE, (300, 100), self.load_game)
            test_game = Text("TEST GAME", const.WHITE, (300, 200), self.dummy_function)
            quit_game = Text("QUIT GAME", const.WHITE, (300, 300), self.quit_game)

            # Draw text on screen
            for text in [start_game] + [test_game] + [quit_game]:
                render = text.draw(screen)
                self.options.append(render)
                self.texts.append(text)

            # Update actors
            pygame.display.update(self.options)


    def load_game(self):
        self.exit = True

    def quit_game(self):
        self.exit = True
        pygame.display.quit()
        pygame.quit()
        sys.exit()

    def dummy_function(self):
        pass

