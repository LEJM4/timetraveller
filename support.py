import pygame
from os import walk
from settings import *
from os.path import join
from os import walk
from pytmx.util_pygame import load_pygame

def import_folder(path):
    surface_list = []

    #durchlauft alle Ordner zum angegebenen Pfad
    for _, __, img_files in walk(path):
        for image in img_files:
            # erstellt den Pfad zur aktuellen Bilddatei
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list

def import_folder(*path):
	frames = []
	for folder_path, sub_folders, image_names in walk(join(*path)):
		for image_name in sorted(image_names, key = lambda name: int(name.split('.')[0])):
			full_path = join(folder_path, image_name)
			surf = pygame.image.load(full_path).convert_alpha()
			frames.append(surf)
	return frames