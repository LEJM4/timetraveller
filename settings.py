import pygame
from pyautogui import size

class Settings:
    def __init__(self):
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.screen = {}
        
    def screen(self):
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.screen = {'small': (800, 600),
                        'medium': (1280, 720),
                        'large': (1920, 1080),
                        'fullscreen': (pygame.display.Info().current_w, pygame.display.Info().current_h) #siehe pygame docs
            }
    
# screen
#SCREEN_WIDTH,SCREEN_HEIGHT = size() #--> Vollbild
#print (SCREEN_WIDTH, SCREEN_HEIGHT)
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

TILE_SIZE = 64 #Tile_Pixel = 64x64


#a = pygame.display.get_desktop_sizes()
#print(a)
# hier kommen dann evtl. noch dict. rein, um den Code in anderen
#Dateien sauberer zu halten 

font_path = 'fonts/Enchanted Land.otf'
#https://www.dafont.com/de/search.php?q=Enchanted+Land