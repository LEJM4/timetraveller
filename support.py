import pygame
from os import walk
from settings import *
from os.path import join
from os import walk
from pytmx.util_pygame import load_pygame
from sys import exit
from pygame.math import Vector2 as vector 



# image and map stuff
def import_image(*path, alpha = True, format = 'png'):
	full_path = join(*path) + f'.{format}'
	surf = pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
	return surf

def import_tilemap(cols, rows, *path):
	frames = {}
	surf = import_image(*path)
	cell_width, cell_height = surf.get_width() / cols, surf.get_height() / rows
	for col in range(cols):
		for row in range(rows):
			cutout_rect = pygame.Rect(col * cell_width, row * cell_height,cell_width,cell_height)
			cutout_surf = pygame.Surface((cell_width, cell_height))
			cutout_surf.fill('green')
			cutout_surf.set_colorkey('green')
			cutout_surf.blit(surf, (0,0), cutout_rect)
			frames[(col, row)] = cutout_surf
	return frames


def character_image_importer_vertical(cols, row, *path):
	frame_dict = import_tilemap(cols, row,*path)
	new_dict ={}
	for row, direction in enumerate(('down','left', 'right','up')):
		new_dict[direction] = [frame_dict[(col, row)] for col in range(int(cols))]
		#new_dict[f'{direction}_idle'] = [frame_dict[(0, row)]]
	return new_dict


def import_multiple_spritesheets(cols, rows, *path, orientation= 'vertical'):
	new_dict = {}
	for _, __, image_names in walk(join(*path)):
		for image in image_names:
			image_name = image.split('.')[0] #teilt ab "." den str in zwei haelften und nimmt nur diie erste
			if orientation == 'vertical':
				new_dict[image_name] = character_image_importer_vertical(cols, rows,*path, image_name)
			elif orientation == 'horizontal':
				new_dict[image_name] = character_image_importer_horizontal(cols, rows,*path, image_name)
	return new_dict


def import_folder_big(*path):
	surf_list = []
	for folder_path, sub_folders, image_names in walk(join(*path)):
		for image_name in sorted(image_names, key = lambda name: int(name.split('.')[0])):
			full_path = join(folder_path, image_name)
			surf = pygame.image.load(full_path).convert_alpha()
			surf_list.append(surf)
	return surf_list



def import_sub_folders(*path):
	frames = {}
	for _, sub_folders, __ in walk(join(*path)):
		if sub_folders:
			for sub_folder in sub_folders:
				frames[sub_folder] = import_folder_big(*path, sub_folder)
	return frames


def tmx_importer(*path):
	tmx_dict = {}
	for folder_path, sub_folders, file_names in walk(join(*path)):
		for file in file_names:
			tmx_dict[file.split('.')[0]] = load_pygame(join(folder_path, file))
	return tmx_dict

def character_image_importer_horizontal(cols, row, *path):
	frame_dict = import_tilemap(cols, row,*path)
	new_dict ={}
	for cols, direction in enumerate(('down','left', 'right','up')):
		new_dict[direction] = [frame_dict[(col, row)] for col in range(int(cols))]
		#new_dict[f'{direction}_idle'] = [frame_dict[(0, row)]]
	return new_dict

'''
pygame.init()
ds = pygame.display.set_mode((1100, 900))

path = 'graphics', 'npc', 'npc_1'
frames = import_multiple_spritesheets(4, 4, *path)
print(frames)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
	ds.fill((0,0,0))
	#ds.blit(aa[0], (0,0))
	pygame.display.update()

#'''



#map 
def check_distance(radius, target, entity):
	distance_vector = (vector(target.rect.center) - vector(entity.rect.center)) 
	#distance_vector = vector vom spieler - vector vom zombie
	# moeglich waere auch:
	# distance_vector = (vector(self.player.rect.center) - vector(self.rect.center)).magnitude() 
	#magnitude : https://pyga.me/docs/ref/math.html#pygame.math.Vector2.magnitude
	# quadriert und zieht die Wurzel --> wurzel ziehen ist fuer computer bloed zu rechnen --> deshalb quadrieren
	# (Danke "dezer_ted")
	distance_squared = distance_vector.length_squared()
	radius_squared = radius**2
	return distance_squared < radius_squared
