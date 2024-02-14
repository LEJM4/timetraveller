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
                #if not image: continue
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
        
        # for tree in tree_layer:
        #     if hasattr(tree, 'image'):
        #         if  tree.image:
        #             image = tree.image
        #             position = (tree.x, tree.y) - self.relocation
        #             self.display_surface.blit(image, position)
        
        for tree in tree_layer:
            Tree((tree.x, tree.y), tree.image, [self.tree_group ])


        for bush in bush_layer:
            Bush((bush.x, bush.y), bush.image, [self.bush_group ])

