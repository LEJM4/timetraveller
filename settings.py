import pygame
from pyautogui import size

class Settings:
    def __init__(self):
        self.resolution_changed = False
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.new_SCREEN_WIDTH = 0
        self.new_SCREEN_HEIGHT = 0
        
    
# screen
#SCREEN_WIDTH,SCREEN_HEIGHT = size() #--> Vollbild
#print (SCREEN_WIDTH, SCREEN_HEIGHT)
i = Settings()

SCREEN_WIDTH = i.SCREEN_WIDTH
SCREEN_HEIGHT = i.SCREEN_HEIGHT

TILE_SIZE = 64 #Tile_Pixel = 64x64


#a = pygame.display.get_desktop_sizes()
#print(a)
# hier kommen dann evtl. noch dict. rein, um den Code in anderen
#Dateien sauberer zu halten 

font_path = 'fonts/Enchanted Land.otf'
#https://www.dafont.com/de/search.php?q=Enchanted+Land