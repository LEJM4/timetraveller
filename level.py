import pygame 
from pytmx.util_pygame import load_pygame
from player import Player
from os.path import join

#from entity import Entity, Player

from camera import Camera
from objects import *
from settings import *

from support import *


class Level:
    def __init__(self, data):
       # self.bu = import_image('graphcis', 'objects', 'projectile', '0')
        self.bu = pygame.image.load('graphics/objects/projectile/left/0.png').convert_alpha()


        #maps



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

        self.star_bullet_group = pygame.sprite.Group()

        self.transition_objects = pygame.sprite.Group()

        self.tile_maps_import()
        self.create_map(self.tile_maps['lvl_1'], 'meadow')
        """
        self.draw_background_normal_layers(tile_map = self.tile_maps['lvl'])
        self.draw_background_object_layers(tile_map= self.tile_maps['lvl'],
                                           player_spawn_pos= 'lvl')
        self.player_spawnpoint(tile_map= self.tile_maps['lvl'])
        #"""

		# transition / tint
        self.transition_destination = None
        self.tint_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.tint_mode = 'untint'
        self.tint_progress = 0
        self.tint_direction = -1
        self.tint_speed = 600

    def tile_maps_import(self):
        self.tile_maps = tmx_importer('map', 'tile_maps')
        '''
        self.tile_maps = {
            'start': load_pygame(join('map', 'tile_maps', 'test_lvl.tmx')),
            'a': load_pygame(join('map', 'tile_maps', 'unbenannt.tmx')),
            'tardis':load_pygame(join('map', 'tile_maps', 'tardis_room.tmx')),
            'lvl': load_pygame(join('map', 'tile_maps', 'lvl_1.tmx')),}

        #'''
            
        self.map_animations = {
            'water' : import_folder_big('graphics', 'ground', 'water',),
            'characters' : import_npc('graphics', 'npc', 'npc_1')      
        }
        #print(self.map_animations['characters'])



    def create_map(self, tile_map, player_start_pos):
        for group in (self.all_sprites, self.obstacle_objects, self.interaction_objects, self.trail, self.star_bullet_group, self.transition_objects):
            group.empty()

        #ground laayers
        for x, y, image in tile_map.get_layer_by_name('ground').tiles():
            General(pos=(x*TILE_SIZE, y*TILE_SIZE), 
                    image= image,
                    groups= [self.all_sprites],
                    z_layer= LAYERS['ground'])
            
        #traail laayer            
        for x,y, image in tile_map.get_layer_by_name('trail').tiles():
            Trail(pos=(x*TILE_SIZE, y*TILE_SIZE), 
                    image= image,
                    groups= [self.all_sprites, self.trail],
                    z_layer= LAYERS['trail'])


        ###creaate all objects

        #tile_map = load_pygame(self.map_string)
        nature_layer = tile_map.get_layer_by_name('nature')
        buildings_layer = tile_map.get_layer_by_name('buildings')

        map_limit_layer = tile_map.get_layer_by_name('map_limit')

        for tile in map_limit_layer:
            General(pos=(tile.x, tile.y), 
                    image= tile.image,
                    groups= [self.obstacle_objects], #nicht zu "all_sprites"--> damit diese nicht gemalt werden
                    z_layer= LAYERS['ground'])
            


        for water in tile_map.get_layer_by_name('water'):
            for x in range (int(water.x), int(water.x + water.width), TILE_SIZE):
                for y in range (int(water.y), int(water.y + water.height), TILE_SIZE):
                    AnimatedSprites(pos = (x,y),
                                    frame_list = self.map_animations['water'],
                                    groups= [self.all_sprites, self.obstacle_objects],
                                    animation_speed= 4)

        for nature_obj in nature_layer:
            if nature_obj.name == ('tree_small'):
                Tree(
                    pos= (nature_obj.x, nature_obj.y), 
                    image= nature_obj.image, 
                    groups= [self.all_sprites, self.obstacle_objects],
                    item_type= 'tree_small')
                
            if nature_obj.name == ('tree_big'):
                Tree(
                    pos= (nature_obj.x, nature_obj.y), 
                    image= nature_obj.image, 
                    groups= [self.all_sprites, self.obstacle_objects],
                    item_type= 'tree_big')
                
            if nature_obj.name == ('transparent_tree'):
                Tree(
                    pos= (nature_obj.x, nature_obj.y), 
                    image= nature_obj.image, 
                    groups= [self.all_sprites],
                    item_type= 'big_tree')

            if nature_obj.name == ('empty'):
                Bush(
                    pos = (nature_obj.x, nature_obj.y), 
                    image = nature_obj.image, 
                    groups = [self.all_sprites], 
                    item_type = 'Empty')

            if nature_obj.name == ('blueberry'):
                Bush(
                    pos = (nature_obj.x, nature_obj.y),
                    image = nature_obj.image, 
                    groups = [self.all_sprites, self.interaction_objects], 
                    item_type = 'Blueberry')

            if nature_obj.name == ('raspberry'):
                Bush(
                    pos = (nature_obj.x, nature_obj.y),
                    image =nature_obj.image, 
                    groups =[self.all_sprites, self.interaction_objects], 
                    item_type= 'Raspberry')

            if nature_obj.name == ('stone'):
                Stone(pos = (nature_obj.x, nature_obj.y),
                    image = nature_obj.image, 
                    groups =[self.all_sprites, self.interaction_objects], 
                    item_type= '')


        for building in buildings_layer:
            if building.name == ('tardis'):
                Tardis(
                    pos = (building.x, building.y),
                    image = building.image, 
                    groups =[self.all_sprites, self.interaction_objects], 
                    item_type= '')
            
            if building.name == ('house_1') or building.name == ('house_2') or building.name == ('house_3'):
                House(
                    pos = (building.x, building.y),
                    image = building.image, 
                    groups =[self.all_sprites, self.interaction_objects, self.obstacle_objects], 
                    item_type= '')
            else:
                General(pos = (building.x, building.y),
                    image = building.image, 
                    groups =[self.all_sprites])
        
        

                
        for obj in tile_map.get_layer_by_name('transition'):
            TransitionObjects(pos= (obj.x, obj.y),
                              size= (obj.width, obj.height),
                              destination= ( obj.properties['destination'], obj.properties['location']),
                              groups= [self.transition_objects]
                              )

        #charaacter + npc

        #___________________________

        for object in tile_map.get_layer_by_name('character'):
                    
                    if object.name == 'player':
                        if object.properties['position'] == player_start_pos:
                            self.player = Player(
                                pos = (object.x, object.y), 
                                groups = self.all_sprites, 
                                status= object.properties['direction'],
                                obstacle_objects= self.obstacle_objects ,
                                interaction_objects= self.interaction_objects, 
                                trail= self.trail,
                                data = self.data,
                                path= ('graphics', 'character'),
                                create_star_bullet= self.star_bullet_player)

                    if object.name == 'trader':
                        pass


    def star_bullet_player(self, pos, direction):#:, path):
        Star(pos= pos,
            direction = direction,
            surf= self.bu,
            groups= [self.all_sprites , self.star_bullet_group])
            
            #path = ('character', 'objects', 'projectile'))

    def bush_collision(self):
        keys = pygame.key.get_pressed()
        #pic item
        if keys[pygame.K_e]:
            if self.player.direction.magnitude() == 0:
                if self.interaction_objects:
                    interaction_objects = pygame.sprite.spritecollide(self.player, self.interaction_objects, False) #(sprite: _HasRect, group: -> hier "interaction_objects", dookill = True --> boolean)
                    if pygame.sprite.spritecollide(self.player, self.interaction_objects, True, pygame.sprite.collide_mask):
                        
                        if interaction_objects:
                            if (interaction_objects[0].item_type) == 'Blueberry':
                                self.player.collision_bush_update('blueberry')
                            
                            if (interaction_objects[0].item_type) == 'Raspberry':
                                self.player.collision_bush_update('raspberry')

                            if (interaction_objects[0].item_type) == 'Coin':
                                self.player.collision_bush_update('coin')
                            print('Collision in lvl.py + Remove object')

    def transition_check(self):
        sprites = [sprite for sprite in self.transition_objects if sprite.rect.colliderect(self.player.hitbox_player)]
        if sprites:
            self.player.block()
            self.transition_destination = sprites[0].destination
            self.tint_mode = 'tint'

    def tint_screen(self, dt):
        if self.tint_mode == 'untint':
            self.tint_progress -= self.tint_speed * dt

        if self.tint_mode == 'tint':
            self.tint_progress += self.tint_speed * dt
            if self.tint_progress >= 255:
                self.create_map(self.tile_maps[self.transition_destination[0]], self.transition_destination[1])
                self.tint_mode = 'untint'
                self.transition_destination = None

        self.tint_progress = max(0, min(self.tint_progress, 255))
        self.tint_surf.set_alpha(self.tint_progress)
        self.display_surface.blit(self.tint_surf, (0,0))

    def run(self,dt):
        #print(self.player.status)

        self.display_surface.fill('purple')
        
        self.transition_check()

        self.bush_collision() # methode muss aufgerufen werden, damit coll. hier fkt
        
        self.all_sprites.update(dt)

        self.all_sprites.draw_all_objects(self.player)

        
        self.tint_screen(dt)