import pygame
from pyautogui import size
from pygame.math import Vector2 as vector 

            
# screen
#SCREEN_WIDTH,SCREEN_HEIGHT = size() #--> Vollbild
#print (SCREEN_WIDTH, SCREEN_HEIGHT)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCALE_FACTOR = 4
TILE_SIZE = 64 #Tile_Pixel = 64x64


missions_text = {'lvl_1': ['Sammle 10 Beeren.' , 'Sprich mit dem Computer.', 'Besuche den großen Baum.'],
           'lvl_2': ['__', '__', '__']}




#button setup
space_between_buttons_y = SCREEN_HEIGHT/20

button_size = {'missions': (SCREEN_WIDTH //4, SCREEN_HEIGHT //14),
               'esc_menu': (1,1)}

button_pos = {'missions': [(20,20),(20, 25 + button_size['missions'][1],),(20, 30+ 2* button_size['missions'][1])]}




print(button_pos['missions'])
LAYERS = {
	'water': 0,
	'ground': 1,
    'trail': 2,
    'gras':3,
	'main': 4,
    'player':5
    }
#a = pygame.display.get_desktop_sizes()
#print(a)
# hier kommen dann evtl. noch dict. rein, um den Code in anderen
#Dateien sauberer zu halten 

font_path = 'fonts/Enchanted Land.otf'
#https://www.dafont.com/de/search.php?q=Enchanted+Land

