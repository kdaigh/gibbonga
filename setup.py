## @file setup.py
#  Setup file containing game asset dictionaries
#
#  Project: Gallaga Clone
#  Author: Py Five
#  Created: 11/19/19

import os.path
import pygame
import tools
import constants as const

pygame.init()
screen = pygame.display.set_mode(const.SCREENRECT.size, 0)

IMAGES = tools.load_all_images(os.path.join("assets", "images"))
SOUNDS = tools.load_all_sounds(os.path.join("assets", "audios"))