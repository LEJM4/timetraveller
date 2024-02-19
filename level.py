import pygame 
from pytmx.util_pygame import load_pygame
from player import Player
from bush import Bush
from camera import Camera
from objects import Tree, Bush, Trail

class Level:
    def __init__(self, data):
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
        
        self.draw_backround_object_layers()
        self.player_spawnpoint()


    def draw_backround_object_layers(self):
        tile_map = load_pygame("map/background_ground.tmx")
        tree_layer = tile_map.get_layer_by_name('Trees')
        bush_layer = tile_map.get_layer_by_name('Bush')

        for tree in tree_layer:
            if tree.name == ('Tree'):
                Tree(
                    pos= (tree.x, tree.y), 
                    image= tree.image, 
                    groups= [self.all_sprites, self.obstacle_objects],
                    item_type= 'normal_tree')
            if tree.name == ('Big_Tree'):
                Tree(
                    pos= (tree.x, tree.y), 
                    image= tree.image, 
                    groups= [self.all_sprites, self.obstacle_objects],
                    item_type= 'Big_tree')

        for bush in bush_layer:
            if bush.name == ('Empty'):
                Bush(
                    pos = (bush.x, bush.y), 
                    image = bush.image, 
                    groups = [self.all_sprites], 
                    item_type = 'Empty')

            if bush.name == ('Blueberry'):
                Bush(
                    pos = (bush.x, bush.y),
                    image = bush.image, 
                    groups = [self.all_sprites, self.interaction_objects], 
                    item_type = 'Blueberry')

            if bush.name == ('Raspberry'):
                Bush(
                    pos = (bush.x, bush.y),
                    image =bush.image, 
                    groups =[self.all_sprites, self.interaction_objects], 
                    item_type= 'Raspberry')



        #draw trail_layer --> damit vel von player erhoeht werden kann
        for x,y, image in tile_map.get_layer_by_name('trail').tiles():
            Trail((x*64,y*64), image, self.trail)

    def player_spawnpoint(self):
        tile_map = load_pygame("map/background_ground.tmx")
        for object in tile_map.get_layer_by_name('Spawn'):
            
            if object.name == 'Player':
                self.player = Player(
                    pos = (object.x, object.y), 
                    groups = self.all_sprites, 
                    obstacle_objects= self.obstacle_objects ,
                    interaction_objects= self.interaction_objects, 
                    trail= self.trail,
                    data = self.data)
                
            if object.name == 'Trader':
                pass
    

    def bush_collision(self):
        keys = pygame.key.get_just_pressed()
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


    def run(self,dt):

        self.all_sprites.update(dt)

		
        self.display_surface.fill('black')

        self.bush_collision() # methode muss aufgerufen werden, damit coll. hier fkt
        
        self.all_sprites.draw_all_objects(self.player)
