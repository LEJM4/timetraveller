import pygame
from os import walk


def import_folder(path):
    surface_list = []

    #durchlauft alle Ordnerzum angegebenen Pfad
    for _, __, img_files in walk(path):
        for image in img_files:
            # erstellt den Pfad zur aktuellen Bilddatei
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list