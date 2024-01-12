import pygame 
#from pytmx.util_pygame import load_pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
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
        self.player = Player((SCREEN_WIDTH, SCREEN_HEIGHT), self.all_sprites)  # Spawnpunkt auf der gesamten Karte
        self.bush = Bush((400,200), self.all_sprites)

    def run(self,dt):


        self.all_sprites.draw_all_objects(self.player)
        self.all_sprites.update(dt)