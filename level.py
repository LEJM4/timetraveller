import pygame 
from pytmx.util_pygame import load_pygame
from settings import *
from player import Player
from bush import Bush
from camera import Camera

class Level:
    def __init__(self):
        #display_surface
        self.display_surface = pygame.display.get_surface()
        
        self.all_sprites = Camera()
        self.setup()

    def setup(self):
        self.player = Player((SCREEN_WIDTH//2,SCREEN_HEIGHT//2), self.all_sprites)
        self.bush = Bush((400,200), self.all_sprites)

    def run(self,dt):


        self.all_sprites.custom_draw()
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)