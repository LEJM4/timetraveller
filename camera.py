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
                
        for i in range (self.backround_ground.width):
            for j in range (self.backround_ground.height):
                image = self.backround_ground.get_tile_image(i, j, 0) # ..._image (x , y , layer)
                self.display_surface.blit(image, (i*64,j*64))

    def custom_draw (self):
        #create the offset
        # self.offset.x = self.player.rect.centerx - SCREEN_WIDTH / 2
        # self.offset.y = self.player.rect - SCREEN_HEIGHT / 2

        #backround_ground
        self.display_surface.blit(self.backround_ground, (0,0))

        #sprites
        for sprite in self.sprites():
            self.display_surface.blit(sprite.image, sprite.rect)
