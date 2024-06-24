from typing import Any
import pygame
from settings import *
from settings import LAYERS

class General(pygame.sprite.Sprite):
    def __init__(self, pos, image, groups, z_layer = LAYERS['main']) :
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect
        self.z_layer = z_layer

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


class PlantParent(pygame.sprite.Sprite):
    def __init__(self, pos, image, groups, z_layer = LAYERS['main']):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect
        self.z_layer = z_layer


class Tree(PlantParent):
    def __init__(self, pos, image, groups, item_type):
        super().__init__(pos, image, groups)
        self.hitbox = self.rect.inflate(-self.rect.width * 0.9 , -self.rect.height*0.2)
        self.item_type = item_type


class Bush(PlantParent):
    def __init__(self, pos, image, groups, item_type):
        super().__init__(pos, image, groups)
        self.item_type = item_type
        self.mask = pygame.mask.from_surface(self.image)

class Trail(PlantParent):
    def __init__(self, pos, image, groups, z_layer=LAYERS['main']):
        super().__init__(pos, image, groups, z_layer)

class Item(pygame.sprite.Sprite):
    def __init__(self, pos, image, groups, item_type):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect
        self.item_type = item_type


class Tardis(PlantParent):
    def __init__(self, pos, image, groups, item_type):
        super().__init__(pos, image, groups)
        self.item_type = item_type
        self.mask = pygame.mask.from_surface(self.image)

class House(PlantParent):
    def __init__(self, pos, image, groups, item_type):
        super().__init__(pos, image, groups)
        self.item_type = item_type
        self.mask = pygame.mask.from_surface(self.image)

class Stone(PlantParent):
    def __init__(self, pos, image, groups, item_type):
        super().__init__(pos, image, groups)
        self.item_type = item_type
        self.mask = pygame.mask.from_surface(self.image)