import pygame
from pytmx.util_pygame import load_pygame
import pytmx
from player import Player
#from bush import Bush
from settings import *
from level import *
from settings import *


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        
        self.tile_map = load_pygame("map/background_ground.tmx")
        self.relocation = pygame.math.Vector2()
        self.display_surface = pygame.display.get_surface()



    def draw_all_objects (self, player):
        #relocating the player

        self.relocation.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.relocation.y = player.rect.centery - SCREEN_HEIGHT / 2
                
        self.draw_backround_normal_layers()
        self.draw_backround_object_layers()
        for sprite in self.sprites():
            self.relocated_position = sprite.rect.topleft - self.relocation
            self.display_surface.blit(sprite.image, self.relocated_position)

    def draw_backround_normal_layers(self):
        
        for index in self.tile_map.visible_tile_layers:
            for x, y, image in self.tile_map.layers[index].tiles():
                if not image: continue
                self.display_surface.blit(image, (x*64,y*64) -self.relocation)
        
    def draw_backround_object_layers(self):
        pass



"""
        ground = t.get_layer_by_name('Ground')
        trail = t.get_layer_by_name('Trail')
        bush = t.get_layer_by_name('bush_2')

        for x, y, image in ground.tiles():
            if not image: continue
            self.display_surface.blit(image, (x*64,y*64) -self.relocation)
            
        
        for x, y, image in trail.tiles():
            if not image: continue
            self.display_surface.blit(image, (x*64,y*64) -self.relocation)

        for x, y, image in bush.tiles():
            if not image: continue
            self.display_surface.blit(image, (x*64,y*64) -self.relocation)
"""

"""
        for x in range (t.width):
            for y in range (t.height):
                image = t.get_tile_image(x, y, layer =1) 
                if image:
                    self.display_surface.blit(image, (x*64,y*64) -self.relocation)

                    """
"""
        print(player.rect.centerx)
        print("")
        print("")
        print(player.rect.centery)
"""
"""
        for x in range (20):
            for y in range (12):
                image = self.backround_ground.get_tile_image(x, y, layer =0) 
                self.display_surface.blit(image, (x*64,y*64))
        
        for x in range (20):
            for y in range (12):
                image = self.backround_ground.get_tile_image(int(self.x_coordinate/64) + x, (int(self.y_coordinate/64) +y, layer =0) 
                self.display_surface.blit(image, (x*64,y*64))

        from pytmx.util_pygame import load_pygame
>>> tmxdata = load_pygame("map.tmx")
tmxdata = load_pygame("map/background_ground.tmx")

"""
