## @file setup.py
#  Setup file containing game asset dictionaries
#
#  Project: Galaga Clone
#  Author: Py Five
#  Created: 11/19/18

import pygame, os.path
from . import tools, constants


pygame.init()
screen = pygame.display.set_mode(constants.SCREENRECT.size, 0)

IMAGES = tools.load_all_images(os.path.join("assets", "images"))
SOUNDS = tools.load_all_sounds(os.path.join("assets", "audios"))
FONTS = tools.load_all_fonts(os.path.join("assets", "fonts"))
