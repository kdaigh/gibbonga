import os
import pygame
import constants as const

#  @pre Image file name has no periods in it
def load_all_images(directory):
    images = {}
    for file in os.listdir(directory):
        if not file.startswith('.'):
            name = file.split('.')[0]
            print(name)
            surface = pygame.image.load(os.path.join(directory, file))
            if surface.get_alpha():
                surface.convert_alpha()
            else:
                surface = surface.convert()
                surface.set_colorkey(const.WHITE)
            images[name] = surface
    return images