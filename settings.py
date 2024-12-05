from pygame.math import Vector2 as vector 
from data import *
from os.path import join
# screen
#SCREEN_WIDTH,SCREEN_HEIGHT = size() #--> Vollbild
#print (SCREEN_WIDTH, SCREEN_HEIGHT)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCALE_FACTOR = 1
TILE_SIZE = 64 #Tile_Pixel = 64x64



font_size = {'dialog' : SCREEN_HEIGHT // 16,
             'missions': SCREEN_HEIGHT / 1600}


#button setup
space_between_buttons_y = SCREEN_HEIGHT/20

button_size = {'missions': (SCREEN_WIDTH //4, SCREEN_HEIGHT //14),
               'esc_menu': (1,1)}

button_pos = {'missions': [(20,20),(20, 25 + button_size['missions'][1],),(20, 30+ 2* button_size['missions'][1])],
              'inventory': [(SCREEN_WIDTH // 6 * 1.5, SCREEN_HEIGHT // 1.18)]}


#WEAPONS
weapon_dict = {'hand': 1,
               'sword':2,
               'pistol': 1}

hit_points = {'player': 5,
              'zombie_1': 6,
              'zombie_2' : 4}

#print(button_pos['missions'])
LAYERS = {
	'water': 0,
	'ground': 1,
    'trail': 2,
    'gras':3,
	'main': 4,
    'top':5,
    'dialog':6
    }
#a = pygame.display.get_desktop_sizes()
#print(a)
# hier kommen dann evtl. noch dict. rein, um den Code in anderen
#Dateien sauberer zu halten 

#font_path = join('fonts','Enchanted Land.otf')
#https://www.dafont.com/de/search.php?q=Enchanted+Land

font_path = join('fonts', 'Meditative.ttf')
#https://www.dafont.com/de/meditative.font