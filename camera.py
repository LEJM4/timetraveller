import pygame
from pytmx.util_pygame import load_pygame
from player import Player
from bush import Bush
from settings import *
from level import *


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.display_surface = pygame.display.get_surface()
        self.backround_ground = load_pygame('map/backround_ground.tmx')
                


    def custom_draw (self):
        for x in range (20):
            for y in range (12):
                image = self.backround_ground.get_tile_image(x, y, layer =0) 
                self.display_surface.blit(image, (x*64,y*64))

