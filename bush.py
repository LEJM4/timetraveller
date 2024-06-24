import pygame
from player import *
from support import *
#from random import choice
#from os import walk

class Bush(pygame.sprite.Sprite):
    def __init__(self, pos, groups, object_group, image = None):
        super().__init__(groups)

        # self.frame_index_bush = 1
        self.object_group = object_group
        self.bush_empty = False 
        self.image = image or pygame.image.load('graphics/objects/bush_tree/blueberry.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.object_group.add(self) 

