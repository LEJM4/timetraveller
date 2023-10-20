import pygame
from player import *
from support import *
from random import choice
from os import walk

class Bush(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

        # self.frame_index_bush = 1 
        self.image = pygame.image.load('graphics/objects/bush/empty.png' )
        self.rect = self.image.get_rect(center=pos) 

