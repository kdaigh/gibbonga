## @file tools.py
#  Tools file containing game utility functions
#
#  Project: Galaga Clone
#  Author: Py Five
#  Created: 11/19/18

import os.path
import pygame
import constants as const


## Loads images for game into dictionary
#  @pre File name has no periods in it
#  @param directory, directory for images
#  @post Images are loaded in dictionary with [key = name]
def load_all_images(directory):
    images = {}
    for file in os.listdir(directory):
        if not file.startswith('.'):
            name = file.split('.')[0]
            surface = pygame.image.load(os.path.join(directory, file))
            if surface.get_alpha():
                surface.convert_alpha()
            else:
                surface = surface.convert()
                surface.set_colorkey(const.WHITE)
            images[name] = surface
    return images

## Loads sound files for game into dictionary
#  @pre File name has no periods in it
#  @param directory, directory for sound assets
#  @post Sound are loaded in dictionary with [key = name]
def load_all_sounds(directory):
    sounds = {}
    for file in os.listdir(directory):
        if not file.startswith('.'):
            name = file.split('.')[0]
            sounds[name] = pygame.mixer.Sound(os.path.join(directory, file))
    return sounds
