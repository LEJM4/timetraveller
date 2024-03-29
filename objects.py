import pygame

class PlantParent(pygame.sprite.Sprite):
    def __init__(self, pos, image, groups):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect


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
    pass

class Item(pygame.sprite.Sprite):
    def __init__(self, pos, image, groups, item_type):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect
        self.item_type = item_type
