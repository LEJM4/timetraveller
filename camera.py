import pygame
from pytmx.util_pygame import load_pygame
from pygame.math import Vector2
from player import Player
#from bush import Bush
from settings import *
from level import *
from settings import *
from objects import Tree, Bush


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        
        #tiled
        self.tile_map = load_pygame("map/background_ground.tmx")
        
        #for camera
        self.relocation = Vector2()
        self.display_surface = pygame.display.get_surface()
        


    def draw_all_objects (self, player):
        #relocating the player

        self.relocation.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.relocation.y = player.rect.centery - SCREEN_HEIGHT / 2
                
        self.draw_backround_normal_layers()

        for sprite in self.sort_sprites():
            self.relocated_position = sprite.rect.topleft - self.relocation
            self.display_surface.blit(sprite.image, self.relocated_position)

    def sort_sprites(self):
        # liste mit sprites nach y-WerteN
        return sorted(self.sprites(), key=self.sprite_sort_key)

    def sprite_sort_key(self, sprite):
        # nach y werten sortieren
        return sprite.rect.centery
    
    
    def draw_backround_normal_layers(self):
        #draw normal layers
        for index in self.tile_map.visible_tile_layers:
            for x, y, image in self.tile_map.layers[index].tiles():
                if not image: continue
                self.display_surface.blit(image, (x*64,y*64) -self.relocation)

        """        
        for normal_layer in ["ground" , "trail"]:
            for x,y, image in self.tile_map.get_layer_by_name(normal_layer).tiles():
                #if not image: continue
                self.display_surface.blit(image, (x*64,y*64) -self.relocation)
        """

                
