import pygame
from player import *
from support import *
from random import choice
from os import walk

class Bush(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)

    def bush(self, pos):
        self.frame_index_bush = 1 
        self.image_bush = pygame.image.load('../graphics/objects/bush/0.png' )
        self.rect_bush = self.image_bush.get_rect(center=pos) 
        
        
        for _, _, img_list_bush in walk('../graphics/objects/bush'):
            bush_choice = choice(img_list_bush)
            
        self.image_bush = pygame.image.load('../graphics/objects/bushes/'+ bush_choice).convert_alpha()
    
