import pygame 
from pytmx.util_pygame import load_pygame
from settings import *
from player import Player
from bush import Bush


class Level:
    def __init__(self):
        #display_surface
        self.display_surface = pygame.display.get_surface()
        self.backround = load_pygame('map/test.tmx')

        

        # sprite groups
        self.all_sprites = pygame.sprite.Group()

        self.setup()

    def setup(self):
        self.player = Player((SCREEN_WIDTH//2,SCREEN_HEIGHT//2), self.all_sprites)
        self.bush = Bush((400,200), self.all_sprites)

    def run(self,dt):
        self.display_surface.fill('black')
        image = self.backround.get_tile_image(0, 0, 0)
        self.display_surface.blit(image, (0,0))

        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)