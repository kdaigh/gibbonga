import os.path
import pygame
import constants as const


#  @pre Image file name has no periods in it
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


#  @pre Image file name has no periods in it
# def load_all_sounds(directory):
#     sounds = {}
#     for file in os.listdir(directory):
#         if not file.startswith('.'):
#             name = file.split('.')[0]
#             sounds[name] = pygame.mixer.Sound(os.path.join(directory, file))
#     return sounds


def load_all_sounds(directory, accept=('.wav','.mpe','.ogg','.mdi')):
    sounds = {}
    for file in os.listdir(directory):
        print(file)
        name, ext = os.path.splitext(file)
        if ext.lower() in accept:
            sounds[name] = pygame.mixer.Sound(os.path.join(directory, file))
    return sounds
