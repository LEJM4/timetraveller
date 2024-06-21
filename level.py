import pygame 
from pytmx.util_pygame import load_pygame
from player import Player
from os.path import join


from bush import Bush
from camera import Camera
from objects import *
from settings import *

class Level:
    def __init__(self, data):
        
        #maps
        #self.map = "map/background_ground.tmx"
        self.map_string = "map/tile_maps/test_lvl.tmx"

        #display_surface
        self.display_surface = pygame.display.get_surface()

        #data 4 the berrys
        self.data = data
        
        #groups
        self.all_sprites = Camera()

        #self.tree_group = pygame.sprite.Group()
        #self.bush_group = pygame.sprite.Group()
        self.obstacle_objects = pygame.sprite.Group()
        self.interaction_objects = pygame.sprite.Group()
        self.trail = pygame.sprite.Group()
        
        self.draw_background_normal_layers()
        self.draw_background_object_layers()
        self.player_spawnpoint()

    
    def draw_background_normal_layers(self):
        #draw normal layers
        tile_map = load_pygame(self.map_string)

        for x, y, image in tile_map.get_layer_by_name('ground').tiles():
            General(pos=(x*TILE_SIZE, y*TILE_SIZE), 
                    image= image,
                    groups= [self.all_sprites],
                    z_layer= LAYERS['ground'])
            
        for x,y, image in tile_map.get_layer_by_name('trail').tiles():
            Trail(pos=(x*TILE_SIZE, y*TILE_SIZE), 
                    image= image,
                    groups= [self.all_sprites, self.trail],
                    z_layer= LAYERS['trail'])
            
        for x, y, image in tile_map.get_layer_by_name('map_limit').tiles():
            General(pos=(x*TILE_SIZE, y*TILE_SIZE), 
                    image= image,
                    groups= [self.all_sprites,self.obstacle_objects], #nicht zu "all_sprites"--> damit diese nicht gemalt werden
                    z_layer= LAYERS['ground'])
            
    def draw_background_object_layers(self):
        tile_map = load_pygame(self.map_string)
        tree_layer = tile_map.get_layer_by_name('tree')
        bush_layer = tile_map.get_layer_by_name('bush')
        buildings_layer = tile_map.get_layer_by_name('buildings')

        for tree in tree_layer:
            if tree.name == ('tree'):
                Tree(
                    pos= (tree.x, tree.y), 
                    image= tree.image, 
                    groups= [self.all_sprites, self.obstacle_objects],
                    item_type= 'normal_tree')
                
            if tree.name == ('big_tree'):
                Tree(
                    pos= (tree.x, tree.y), 
                    image= tree.image, 
                    groups= [self.all_sprites, self.obstacle_objects],
                    item_type= 'big_tree')
                
            if tree.name == ('transparent_tree'):
                Tree(
                    pos= (tree.x, tree.y), 
                    image= tree.image, 
                    groups= [self.all_sprites],
                    item_type= 'big_tree')

        for bush in bush_layer:
            if bush.name == ('empty'):
                Bush(
                    pos = (bush.x, bush.y), 
                    image = bush.image, 
                    groups = [self.all_sprites], 
                    item_type = 'Empty')

            if bush.name == ('blueberry'):
                Bush(
                    pos = (bush.x, bush.y),
                    image = bush.image, 
                    groups = [self.all_sprites, self.interaction_objects], 
                    item_type = 'Blueberry')

            if bush.name == ('raspberry'):
                Bush(
                    pos = (bush.x, bush.y),
                    image =bush.image, 
                    groups =[self.all_sprites, self.interaction_objects], 
                    item_type= 'Raspberry')
        
        for building in buildings_layer:
            if building.name == ('tardis'):
                Tardis(
                    pos = (building.x, building.y),
                    image = building.image, 
                    groups =[self.all_sprites, self.interaction_objects], 
                    item_type= '')
            
            if building.name == ('house_1'):
                House(
                    pos = (building.x, building.y),
                    image = building.image, 
                    groups =[self.all_sprites, self.interaction_objects], 
                    item_type= '')
                


    def player_spawnpoint(self):
        tile_map = load_pygame(self.map_string)
        for object in tile_map.get_layer_by_name('player'):
            
            if object.name == 'spawn':
                self.player = Player(
                    pos = (object.x, object.y), 
                    groups = self.all_sprites, 
                    obstacle_objects= self.obstacle_objects ,
                    interaction_objects= self.interaction_objects, 
                    trail= self.trail,
                    data = self.data)
                
            if object.name == 'trader':
                pass
    
    
    def obstacle_collision(self):
        for obstacle in self.obstacle_objects:
            pass

    def bush_collision(self):
        keys = pygame.key.get_pressed()
        #pic item
        if keys[pygame.K_e]:
            if self.player.direction.magnitude() == 0:
                if self.interaction_objects:
                    interaction_objects = pygame.sprite.spritecollide(self.player, self.interaction_objects, False) #(sprite: _HasRect, group: -> hier "interaction_objects", dookill = True --> boolean)
                    if pygame.sprite.spritecollide(self.player, self.interaction_objects, True, pygame.sprite.collide_mask):
                        self.player.status = 'collect_up'
                        print(self.player.status)
                        
                        if interaction_objects:
                            if (interaction_objects[0].item_type) == 'Blueberry':
                                self.player.collision_bush_update('blueberry')
                            
                            if (interaction_objects[0].item_type) == 'Raspberry':
                                self.player.collision_bush_update('raspberry')

                            if (interaction_objects[0].item_type) == 'Coin':
                                self.player.collision_bush_update('coin')
                            print('Collision in lvl.py + Remove object')


    def run(self,dt):
        #print(self.player.status)


		
        self.display_surface.fill('black')

        self.bush_collision() # methode muss aufgerufen werden, damit coll. hier fkt
        
        self.all_sprites.draw_all_objects(self.player)

        self.all_sprites.update(dt)