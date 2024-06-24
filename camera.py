import pygame
from pytmx.util_pygame import load_pygame
from pygame.math import Vector2
from player import Player
#from bush import Bush
from settings import *
#from level import *
from objects import *


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        
        #tiled
       
        #for camera
        self.relocation = Vector2()
        self.display_surface = pygame.display.get_surface()
        


    def draw_all_objects (self, player):
        #relocating the player

        self.relocation.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.relocation.y = player.rect.centery - SCREEN_HEIGHT / 2
                
        
        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z_layer == layer:
                    self.relocated_position = sprite.rect.topleft - self.relocation
                    self.display_surface.blit(sprite.image, self.relocated_position)

    def sort_sprites(self):
        # liste mit sprites nach y-WerteN
        return sorted(self.sprites(), key=self.sprite_sort_key)

    def sprite_sort_key(self, sprite):
        # nach y werten sortieren
        return sprite.rect.centery


                
