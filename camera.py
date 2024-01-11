import pygame
from pytmx.util_pygame import load_pygame
from player import Player
from bush import Bush
from settings import *
from level import *
from settings import *


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.relocation = pygame.math.Vector2()
        self.display_surface = pygame.display.get_surface()
        self.background_ground =  pygame.image.load('map/background_ground.png').convert()
                


    def draw_all_objects (self):
        #relocating the player

        #self.relocation.x = player.rect.centerx - SCREEN_WIDTH / 2
        #self.relocation.y = player.rect.centery - SCREEN_HEIGHT / 2
                
        self.display_surface.blit(self.background_ground, (0,0))
        for sprite in self.sprites():
            relocated_position = sprite.rect.topleft + self.relocation
            self.display_surface.blit(sprite.image, relocated_position)

"""
        for x in range (20):
            for y in range (12):
                image = self.backround_ground.get_tile_image(x, y, layer =0) 
                self.display_surface.blit(image, (x*64,y*64))
"""
