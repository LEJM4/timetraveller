import pygame
from settings import *
from settings import LAYERS
from support import *


class General(pygame.sprite.Sprite):
    def __init__(self, pos, image, groups, z_layer = LAYERS['main']) :
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect
        self.z_layer = z_layer
        self.mask = pygame.mask.from_surface(self.image)


class AnimatedSprites(General):
    def __init__(self, pos, frame_list, groups, animation_speed, z_layer=LAYERS['main']):
        self.frame_index = 0
        self.frames = frame_list
        self.animation_speed = animation_speed
        super().__init__(pos, frame_list[self.frame_index], groups, z_layer)
    
    def animation(self,dt):
        self.frame_index += self.animation_speed * dt #Zahl enspricht der schnelligkeit der Bilder fuer die Animation
        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animation(dt)


class NatureSprite(General):
    def __init__(self, pos, image, groups,  item_type= None, z_layer=LAYERS['main']):
        super().__init__(pos, image, groups, z_layer)
        self.item_type = item_type


class Tree(NatureSprite):
    def __init__(self, pos, image, groups, item_type, z_layer=LAYERS['main']):
        super().__init__(pos, image, groups, item_type, z_layer)
        self.hitbox = self.rect.inflate(-self.rect.width * 0.9 , -self.rect.height*0.2)

class Trail(General):
    def __init__(self, pos, image, groups, z_layer=LAYERS['main']):
        super().__init__(pos, image, groups, z_layer)

class Item(General):
    def __init__(self, pos, image, groups, item_type, z_layer=LAYERS['main']):
        super().__init__(pos, image, groups, z_layer)
        self.item_type = item_type

class Star(pygame.sprite.Sprite):
    def __init__(self, pos, direction, frames,animation_speed, groups, z_layer = LAYERS['main']):
        super().__init__(groups)
        self.image = frames
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)

        self.z_layer = z_layer

        self.pos = vector(self.rect.center)
        self.direction = direction
        self.animation_speed = animation_speed
        self.speed = 400
    
    def animation(self, dt):
        pass
    
    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = (round(self.pos.x), round(self.pos.y))


class TransitionObjects(General):
    def __init__(self, pos, size, destination, groups,  z_layer=LAYERS['main']):
        image = pygame.Surface(size)
        super().__init__(pos, image, groups, z_layer)
        self.destination = destination

