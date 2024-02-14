import pygame
from pytmx.util_pygame import load_pygame
from pygame.math import Vector2
from player import Player
#from bush import Bush
from settings import *
from level import *
from settings import *


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
        self.draw_backround_object_layers()

        for sprite in self.sprites():
            self.relocated_position = sprite.rect.topleft - self.relocation
            self.display_surface.blit(sprite.image, self.relocated_position)

            

    def draw_backround_normal_layers(self):
        #draw normal layers
        
        """
        for index in self.tile_map.visible_tile_layers:
            for x, y, image in self.tile_map.layers[index].tiles():
                if not image: continue
                self.display_surface.blit(image, (x*64,y*64) -self.relocation)
        """
                
        for normal_layer in ["ground" , "trail"]:
            for x,y, image in self.tile_map.get_layer_by_name(normal_layer).tiles():
                if not image: continue
                self.display_surface.blit(image, (x*64,y*64) -self.relocation)
        
        #draw the objects in object_layers
                
        # object_layer = self.tile_map.get_layer_by_name('Trees')
        
        # for object in object_layer:
        #     if hasattr(object, 'image'):
        #         if  object.image:
        #             image = object.image
        #             position = (object.x, object.y) - self.relocation
        #             self.display_surface.blit(image, position) 
        
    def draw_backround_object_layers(self):
        tree_layer = self.tile_map.get_layer_by_name('Trees')
        bush_layer = self.tile_map.get_layer_by_name('Bush')
        
        for tree in tree_layer:
            if hasattr(tree, 'image'):
                if  tree.image:
                    image = tree.image
                    position = (tree.x, tree.y) - self.relocation
                    self.display_surface.blit(image, position)
        
        for bush in bush_layer:
           if hasattr(bush, 'image'):
                if  bush.image:
                    image = bush.image
                    position = (bush.x, bush.y) - self.relocation
                    self.display_surface.blit(image, position)
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
