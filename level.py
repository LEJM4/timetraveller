import pygame 
from pytmx.util_pygame import load_pygame
from player import Player
from zombie import Zombie_1, Zombie_2
from os.path import join
from game_data import *
import sys
from timer import Timer

from camera import Camera
from objects import *
from settings import *

from support import *
from missions import UserInterface
from user_interface import Overlay

from dialog import *

# level class mit die wichtigste datei
# verwaltet zentral die geschenisse und ueberprueft die ereignisse
# wenn man sich in ruhe die karte angucken moechte --> dann in "settings.py" --> spieler leben hoch oder zombie leben auf 0

class Level:
    def __init__(self, data):
        self.dialog_tree = None

        #display_surface
        self.display_surface = pygame.display.get_surface() #display surf

        #data 4 the berrys
        self.data = data
        
        self.ui = UserInterface('lvl_1')


        #groups
        self.all_sprites = Camera()
        #self.tree_group = pygame.sprite.Group()
        #self.bush_group = pygame.sprite.Group()
        self.obstacle_objects = pygame.sprite.Group()
        self.interaction_objects = pygame.sprite.Group()
        self.trail = pygame.sprite.Group()
        self.dialog_sprites = pygame.sprite.Group()

        self.projectile_group = pygame.sprite.Group()

        self.transition_objects = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        self.import_tilemaps_and_game_assets() #importieren der daten
        self.create_map(self.tile_maps['lvl_1'], 'meadow') # tilemap nach methode erschaffen


        self.overlay = Overlay() # overlay class hinzufuegen


		# transition / tint
        self.transition_destination = None #tint setup
        self.tint_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.tint_mode = 'untint'
        self.tint_progress = 0
        self.tint_direction = -1
        self.tint_speed = 600

        self.timers = {'player_death': Timer(duration=  (1500), # ist dafuer da, dass sich das spiel, wenn der spieler stirbt beendet
                                            repeat = False,
                                            autostart= False,
                                            func =self.end_game),}

#_________________________________________________________________________________________________________________________
# NICHT MEHR VERAENDERN !!!!

    def import_tilemaps_and_game_assets(self):
        # importieren aller tilemaps --> alle karten auf denen man spielen kann
        self.tile_maps = tmx_importer('map', 'tile_maps')

        #importieren von allen animationen
        self.map_animations = {
            # import der wasser animation
            'water': import_animation_frames(4, 1, 'graphics', 'ground', 'water','water_spritesheet'),

            # import der spieler assets
            'player': {'attack': spritesheet_vertical(4,4, 'graphics','characters', 'player', 'attack'), 
                       'collect': spritesheet_vertical(7,4, 'graphics','characters', 'player', 'collect'), 
                       'idle': spritesheet_vertical(1,4, 'graphics','characters', 'player', 'idle'), 
                       'move': spritesheet_vertical(8,4, 'graphics','characters', 'player', 'move')},
            
            # import der monster assets
            'monster': {'attack': spritesheet_vertical(4,4, 'graphics','characters', 'monster', 'attack'), 
                        'idle': spritesheet_vertical(4,4, 'graphics','characters', 'monster', 'idle'), 
                        'move': spritesheet_vertical(4,4, 'graphics','characters', 'monster', 'move')},
                        
            'skeleton': import_character_animation(4,7, 'graphics','characters', 'monster','Skeleton_SpriteSheet', scale = 3),

            #import der projectile animation
            'projectiles': {'purple_flash': spritesheet_vertical(4,4, 'graphics','objects','projectile','purple_flash_spritesheet')}
        }
        self.fonts = {'dialog': pygame.font.Font(font_path, font_size['dialog'])}
        
    # BIS HIERHIN
#_________________________________________________________________________________________________________________________ 


    def create_map(self, tile_map, player_start_pos):
    # die methode ist dafuer da alle sprites zu erschaffen --> alle object und tile layer
    # es wird ueberprueft ob dieser layer (in tiled) existiert 
        #alle gruppen leeren
        for group in (self.all_sprites, self.obstacle_objects, self.interaction_objects, self.trail, self.projectile_group, self.transition_objects):
            group.empty()
        
        tile_layer_names = {layer.name for layer in tile_map.visible_layers}
        object_layer_names = {layer.name for layer in tile_map.objectgroups}


        #ground laayers
        if 'ground' in tile_layer_names:
            for x, y, image in tile_map.get_layer_by_name('ground').tiles():
                General(pos= (x * TILE_SIZE, y * TILE_SIZE),
                        image= image,
                        groups= [self.all_sprites],
                        z_layer= LAYERS['ground'])
                

                # General(pos=(x * TILE_SIZE * SCALE_FACTOR, y * TILE_SIZE * SCALE_FACTOR),
                #         image= pygame.transform.scale_by(image, SCALE_FACTOR),
                #         groups=[self.all_sprites],
                #         z_layer=LAYERS['ground'])
                                   
        #trail laayer            
        if 'trail' in tile_layer_names:
            for x, y, image in tile_map.get_layer_by_name('trail').tiles():
                Trail(pos=(x * TILE_SIZE, y * TILE_SIZE),
                        image=image,
                        groups=[self.all_sprites, self.trail],
                        z_layer=LAYERS['trail'])

                # Trail(pos=(x * TILE_SIZE * SCALE_FACTOR, y * TILE_SIZE * SCALE_FACTOR),
                #         image= pygame.transform.scale_by(image, SCALE_FACTOR),
                #         groups=[self.all_sprites],
                #         z_layer=LAYERS['ground'])

        #map_limit
        if 'map_limit' in tile_layer_names:
            map_limit_layer = tile_map.get_layer_by_name('map_limit')
            for tile in map_limit_layer:
                General(pos=(tile.x, tile.y),
                        image=tile.image,
                        groups=[self.obstacle_objects],  # #nicht zu "all_sprites"--> damit diese nicht gemalt werden
                        z_layer=LAYERS['ground'])

                # General(pos=(x * TILE_SIZE * SCALE_FACTOR, y * TILE_SIZE * SCALE_FACTOR),
                #         image= pygame.transform.scale_by(image, SCALE_FACTOR),
                #         groups=[self.obstacle_objects],
                #         z_layer=LAYERS['ground'])


        ###creaate all objects
        #water layer
        if 'water' in tile_layer_names:
            for water in tile_map.get_layer_by_name('water'):
                for x in range(int(water.x), int(water.x + water.width), TILE_SIZE):
                    for y in range(int(water.y), int(water.y + water.height), TILE_SIZE):
                        AnimatedSprites(pos=(x, y),
                                        frame_list=self.map_animations['water'],
                                        groups=[self.all_sprites, self.obstacle_objects],
                                        animation_speed=4)

                        # AnimatedSprites(pos=(x * TILE_SIZE * SCALE_FACTOR, y * TILE_SIZE * SCALE_FACTOR),
                        # frame_list = [pygame.transform.scale_by(image, SCALE_FACTOR) for image in frame_list]
                        #         groups= [self.all_sprites, self.obstacle_objects],
                        #         z_layer=LAYERS['ground'])

        #nature layer
        if 'nature' in object_layer_names:
            nature_layer = tile_map.get_layer_by_name('nature')
            for nature_obj in nature_layer:
                if nature_obj.name == 'tree_small':
                    Tree(pos=(nature_obj.x, nature_obj.y),
                            image=nature_obj.image,
                            groups=[self.all_sprites, self.obstacle_objects],
                            item_type='tree_small')
                elif nature_obj.name == 'tree_big':
                    Tree(pos=(nature_obj.x, nature_obj.y),
                            image=nature_obj.image,
                            groups=[self.all_sprites, self.obstacle_objects],
                            item_type='tree_big')
                elif nature_obj.name == 'transparent_tree':
                    Tree(pos=(nature_obj.x, nature_obj.y),
                            image=nature_obj.image,
                            groups=[self.all_sprites],
                            item_type='big_tree')
                elif nature_obj.name == 'empty':
                    NatureSprite(pos=(nature_obj.x, nature_obj.y),
                            image=nature_obj.image,
                            groups=[self.all_sprites],
                            item_type='Empty')
                elif nature_obj.name == 'blueberry':
                    NatureSprite(pos=(nature_obj.x, nature_obj.y),
                            image=nature_obj.image,
                            groups=[self.all_sprites, self.interaction_objects],
                            item_type='Blueberry')
                elif nature_obj.name == 'raspberry':
                    NatureSprite(pos=(nature_obj.x, nature_obj.y),
                            image=nature_obj.image,
                            groups=[self.all_sprites, self.interaction_objects],
                            item_type='Raspberry')
                elif nature_obj.name == 'stone':
                    NatureSprite(pos=(nature_obj.x, nature_obj.y),
                            image=nature_obj.image,
                            groups=[self.all_sprites])
                else:
                    General(pos=(nature_obj.x, nature_obj.y),
                            image=nature_obj.image,
                            groups=[self.all_sprites, self.obstacle_objects])
        #building layer
        if 'buildings' in object_layer_names:
            buildings_layer = tile_map.get_layer_by_name('buildings')
            for building in buildings_layer:
                General(pos=(building.x, building.y),
                        image=building.image,
                        groups=[self.all_sprites, self.obstacle_objects])
            
        #transition
        if 'transition' in object_layer_names:
            transition_layer = tile_map.get_layer_by_name('transition')
            for obj in transition_layer:
                TransitionObjects(pos=(obj.x, obj.y),
                                    size=(obj.width, obj.height),
                                    destination=(obj.properties['destination'], obj.properties['location']),
                                    groups=[self.transition_objects])

    
    # characters Layer
        if 'character' in object_layer_names:
            character_layer = tile_map.get_layer_by_name('character')
            for object in character_layer:
                if object.name == 'player':
                    if object.properties['position'] == player_start_pos:
                        self.player = Player(pos=(object.x, object.y),
                                                groups=self.all_sprites,
                                                frames= self.map_animations['player'],
                                                facing_direction=object.properties['direction'],
                                                obstacle_objects=self.obstacle_objects,
                                                interaction_objects=self.interaction_objects,
                                                trail=self.trail,
                                                data=self.data,
                                                id=object.properties['entity_id'],
                                                create_projectile=self.projectile)

                elif object.name == 'zombie_1':
                    self.zombie = Zombie_1(pos=(object.x, object.y),
                                            groups=[self.all_sprites, self.enemy_group],
                                            frames= self.map_animations['skeleton'],
                                            facing_direction=object.properties['direction'],
                                            obstacle_objects=self.obstacle_objects,
                                            data=self.data,
                                            player=self.player,
                                            id=object.properties['entity_id'])

                elif object.name == 'zombie_2':
                    self.zombie = Zombie_2(pos=(object.x, object.y),
                                            groups=[self.all_sprites, self.enemy_group],
                                            frames= self.map_animations['skeleton'],
                                            facing_direction=object.properties['direction'],
                                            obstacle_objects=self.obstacle_objects,
                                            data=self.data,
                                            player=self.player,
                                            create_projectile=self.projectile,
                                            id=object.properties['entity_id'])

                elif object.name == 'robo':
                    self.robo = Robo(pos=(object.x, object.y),
                                        groups=[self.all_sprites, self.dialog_sprites],
                                        player=self.player,
                                        character_data=Character_DATA[object.properties['character_id']],
                                        create_dialog=self.create_dialog)


    def projectile(self, pos, direction, pointing_direction): # das wird an charactere uebergeben
        Projectile(pos= pos,
            direction = direction,
            frames= self.map_animations['projectiles']['purple_flash'][pointing_direction],
            groups= [self.all_sprites , self.projectile_group],
            animation_speed=4)



    def projectile_collision(self):
        # ueberprueft collision des projectiles --> damit, wenn es auf ein objekt trifft entfernt wird
        for obj in self.obstacle_objects.sprites():
            pygame.sprite.spritecollide(obj, self.projectile_group, True)

        for projectile in self.projectile_group.sprites(): #.sprites() gibt eine liste von sprites zurueck
            monster_sprites = pygame.sprite.spritecollide(projectile, self.enemy_group, False, pygame.sprite.collide_mask)
            if monster_sprites:
                projectile.kill()
                for sprite in monster_sprites:
                    sprite.damage('pistol')
            
            pygame.sprite.spritecollide(obj, self.projectile_group, True)
        #projectiles = [projectile for projectile in self.projectile_group if projectile.rect.colliderect(self.player.hitbox_player)]
        if pygame.sprite.spritecollide(self.player, self.projectile_group, True , pygame.sprite.collide_mask):
           self.player.damage('pistol')



    def trail_collision(self): # ueberprueft ob der spieler sich auf dem weg befindet
        for trail in self.trail.sprites():
            if trail.hitbox.colliderect(self.player.hitbox_player):
                self.player.speed = SPEED_SETTINGS['trail']
                #self.change_speed = True
                break
            else:
                self.speed = SPEED_SETTINGS['player']
                #self.change_speed = False


    def bush_collision(self): # bush collision wichtig, damit er auch die beeren einsammeln kann
        keys = pygame.key.get_just_pressed() 
        sprites = [sprite for sprite in self.interaction_objects if sprite.rect.colliderect(self.player.hitbox_player)]
            #suche nach obj in `interaction_objects` welche mit spieler kollidieren
        #suche nach obj in `interaction_objects` welche mit spieler kollidieren
        if sprites:
            self.player.interaction_objects_collide = True
            if keys[pygame.K_q]: #ueberpruefen ob 'q' gedrueckt wird
            #wenn gefunden
                item = sprites[0]
                item_type = item.item_type.lower() #item type extrahieren
                item.kill() #object entfernen
                
                if item_type in ['blueberry', 'raspberry', 'coin']: #gueltigkeit von item type ueberpruefen
                    self.update_inventory_values(item_type) #zu player_inventory hinzufuegen
                    print(player_inventory)
        else: 
            self.player.interaction_objects_collide = False


    def update_inventory_values(self, item): # ueberprueft ob neue items hinzugefuegt werden muessen
        if item == 'blueberry':
            player_inventory[item] += 1
        
        elif item == 'blueberry':
            player_inventory[item] += 1
        
        elif item == 'blueberry':
            player_inventory[item] += 1


    def transition_check(self): # transition ist das, wenn eine neue karte erschaffen werden muss --> objekte in tiled
        keys = pygame.key.get_just_pressed()
        sprites = [sprite for sprite in self.transition_objects if sprite.rect.colliderect(self.player.hitbox_player)]
        if sprites:
            self.player.transition_collision = True
            if keys[pygame.K_e]:
                self.player.block()
                self.transition_destination = sprites[0].destination
                self.tint_mode = 'tint'
        else:
            self.player.transition_collision = False
            


    def tint_screen(self, dt): # faerbt den screen nach und nach schwarz
        if self.tint_mode == 'untint':
            self.tint_progress -= self.tint_speed * dt
        

        if LIFE_DATA['player']['defeated']: # wenn spieler tot ist dann wird der screen schwarz
            self.tint_mode = 'tint' 

        if self.tint_mode == 'tint':
            self.tint_progress += self.tint_speed * dt
            if LIFE_DATA['player']['defeated'] == False:
                if self.tint_progress >= 255:
                    self.create_map(self.tile_maps[self.transition_destination[0]], self.transition_destination[1])
                    self.tint_mode = 'untint'
                    self.transition_destination = None

        self.tint_progress = max(0, min(self.tint_progress, 255))
        self.tint_surf.set_alpha(self.tint_progress)
        self.display_surface.blit(self.tint_surf, (0,0))


    def input(self): # ueberprueft den input
        if not self.dialog_tree:
            keys = pygame.key.get_just_pressed()
            if keys[pygame.K_RETURN]:
                for object in self.dialog_sprites:
                    print(object)
                    if check_distance(200, self.player, object):
                        if object.character_data['can_talk']:
                            self.player.block()
                            self.create_dialog(object)


    def create_dialog(self, object): # dialog wichtig fuer den roboter
        if not self.dialog_tree:
            self.player.noticed = False
            self.player.status = 'idle'
            self.dialog_tree = DialogTree(object, self.player, self.all_sprites, self.fonts['dialog'], self.end_dialog)


    def end_dialog(self, character):
        # beendet den dialog
        #print(Character_DATA[character.character_data]['dialog'][1])
        Character_DATA['robo']['can_talk'] = False
        character.character_data['can_talk'] = False
        self.dialog_tree = None
        self.player.in_dialog = False
        self.player.unblock()
    
    def end_game(self): # methode, damit sich das game beendet --> wird in self.timers verwendet
        pygame.quit() # beenden von pygame
        sys.exit() # beenden des programms  


    def update_missions(self):
        if player_inventory['blueberry'] + player_inventory['raspberry'] >= 4:
            lvl[1] = True
        
        if Character_DATA['robo']['can_talk'] == False:
            lvl[2] = True
            
        if player_inventory['corps'] >= 3:
            lvl[3] = True

    def update_timer(self):
        for timer in self.timers.values():
            timer.update()

    def run(self,dt):
        self.display_surface.fill('purple')

        self.update_timer()


        # ingame activity
        self.input() #input ueberpruefen
        self.transition_check() #transition ueberpruefen
        self.bush_collision()  #bush_collision ueberpruefen
        self.projectile_collision() #projectile_collision ueberpruefen
        #self.trail_collision() #trail_collision ueberpruefen


        #update
        self.all_sprites.update(dt) #update all_sprites


        # graphical
        self.all_sprites.draw_all_objects(self.player, dt) #zuerst die denn darauf muessen noch gezeichnet werden:
        self.ui.display() #missionen anzeigen: links oben
        self.overlay.display() # leben anzeigen: rechts oben
        self.tint_screen(dt) # gesamter bildschirm
        


        self.update_missions() #passiert was in "data.py"
        if self.dialog_tree: self.dialog_tree.update() #fuer den dialog

        if LIFE_DATA['player']['defeated'] == False:
            self.timers['player_death'].activate()