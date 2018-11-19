import os
import pygame
import tools
import constants as const

pygame.init()
screen = pygame.display.set_mode(const.SCREENRECT.size, 0)

IMAGES = tools.load_all_images(os.path.join("assets", "images"))