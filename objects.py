import pygame


class Tree(pygame.sprite.Sprite):
    def __init__(self, pos, image, groups, item_type):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect
        self.item_type = item_type


class Bush(pygame.sprite.Sprite):
    def __init__(self, pos, image, groups, item_type):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect
        self.item_type = item_type

class Trail(pygame.sprite.Sprite):
    def __init__(self, pos, image, groups):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect

class Item(pygame.sprite.Sprite):
    def __init__(self, pos, image, groups, item_type):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect
        self.item_type = item_type
