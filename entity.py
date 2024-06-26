from settings import *
from support import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, frames , groups, facing_direction):
        super().__init__(groups)
        
        #graphics
        self.frame_index, self.frames = 0, frames
        self.facing_direction = facing_direction

        #sprite
        self.image = self.frames['down'][self.frame_index]
        self.rect = self.image.get_rect(center = pos)

        #other
        self.animation_speed = 6
    
    def animation(self,dt):
        self.frame_index += self.animation_speed * dt #Zahl enspricht der schnelligkeit der Bilder fuer die Animation
        if self.frame_index >= len(self.frames[self.current_state]):
            self.frame_index = 0

        self.image = self.frames[self.current_state()][int(self.frame_index)]

    def current_state(self):
        
        return 'left'
    
class Entity_M(pygame.sprite.Sprite):
    def __init__(self, pos, groups,	facing_direction, obstacle_objects, data, path):
        super().__init__(groups)
        		# 

		# 
        self.path = path

        # graphic
        self.import_pictures_4_animation()
        self.status = facing_direction
        self.frame_index = 0
        self.anmation_speed = 10
        self.z_layer = LAYERS['main']


        #imports
        self.data = data

        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)



        # movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.change_speed = False
        self.speed = 100

        self.blocked = False


        # collision
        self.hitbox_player = self.rect
        self.player_mask = pygame.mask.from_surface(self.image)

        #Parametergroups
        self.obstacle_objects = obstacle_objects


        #attack
        self.attacking = False


	
    def import_pictures_4_animation(self):
        # alle animaatonen mithiilfe der funktiion "subfolder" laden
        self.animations = import_sub_folders(*self.path)
