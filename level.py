import pygame 
from pytmx.util_pygame import load_pygame
from player import Player
from bush import Bush
from camera import Camera
from objects import Tree, Bush

class Level:
    def __init__(self):
        #display_surface
        self.display_surface = pygame.display.get_surface()
        
        #groups
        self.all_sprites = Camera()

        self.tree_group = pygame.sprite.Group()
        self.bush_group = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.interaction_objects = pygame.sprite.Group()
        
        self.draw_backround_object_layers()
        self.player_spawnpoint()


    def draw_backround_object_layers(self):
        tile_map = load_pygame("map/background_ground.tmx")
        tree_layer = tile_map.get_layer_by_name('Trees')
        bush_layer = tile_map.get_layer_by_name('Bush')

        for tree in tree_layer:
            Tree((tree.x, tree.y), tree.image, [self.all_sprites, self.obstacles ,self.tree_group ])

        for bush in bush_layer:
            Bush((bush.x, bush.y), bush.image, [self.all_sprites, self.bush_group, self.interaction_objects])


    def player_spawnpoint(self):
        tile_map = load_pygame("map/background_ground.tmx")
        for object in tile_map.get_layer_by_name('Spawn'):
               if object.name == 'Player':
                   self.player = Player((object.x, object.y), self.all_sprites, self.obstacles ,self.interaction_objects)

    def run(self,dt):

        self.all_sprites.update(dt)

		
        self.display_surface.fill('black')
        
        self.all_sprites.draw_all_objects(self.player)
