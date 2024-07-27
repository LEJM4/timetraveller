from settings import *
from objects import *

class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.relocation = vector()
        self.display_surface = pygame.display.get_surface()
        self.icon_e_original = import_image('graphics', 'ui', 'e-button-icon')
        self.icon_e = self.icon_e_original  

    def draw_all_objects(self, player):
        # relocate player
        self.relocation.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.relocation.y = player.rect.centery - SCREEN_HEIGHT / 2

        # skaliert icon auf breite des spielers
        player_width = player.rect.width
        self.icon_e = pygame.transform.scale(self.icon_e_original, (player_width, self.icon_e_original.get_height()))

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z_layer == layer:
                    self.relocated_position = sprite.rect.topleft - self.relocation
                    self.display_surface.blit(sprite.image, self.relocated_position)

                # if transition --> blit "e"
                if sprite == player and player.transition_collision:
                    icon_position = player.rect.midtop - vector(self.icon_e.get_width() / 2, self.icon_e.get_height() + 10)
                    self.display_surface.blit(self.icon_e, icon_position - self.relocation)

    def sort_sprites(self):
        return sorted(self.sprites(), key=self.sprite_sort_key)

    def sprite_sort_key(self, sprite):
        return sprite.rect.centery
