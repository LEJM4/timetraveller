from settings import *
from objects import *
from dialog import DialogSprite
from geometrie import Circle

class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.relocation = vector()
        self.display_surface = pygame.display.get_surface()
        self.icon_e_original = import_image('graphics', 'ui', 'e_button_icon_0')
        #source:   https://uxwing.com/e-alphabet-round-icon/
        self.icon_e = self.icon_e_original  

        self.icon_e_frames = [
            import_image('graphics', 'ui', 'e_button_icon_0'),
            import_image('graphics', 'ui', 'e_button_icon_1')
        ]

        self.icon_e_animation = AnimatedSprites(
            pos=(0, 0),  # position wird spaeter angepasst
            frame_list=self.icon_e_frames,
            groups=[],  # keine gruppen erforderlich, da  blit verwendet wird
            animation_speed=1.2  # geschwindigkeit der animation
        )

    def draw_all_objects(self, player, dt):
        # relocate player
        self.relocation.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.relocation.y = player.rect.centery - SCREEN_HEIGHT / 2

        # skaliert icon auf breite des spielers
        player_width = player.rect.width
        self.icon_e_animation.frames = [pygame.transform.scale(frame, (player_width, frame.get_height())) for frame in self.icon_e_animation.frames] 
        #skaliert alle frames in der  liste --> oben
        self.icon_e_animation.update(dt) 
        #aktualisiert animation einmal pro frame


        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z_layer == layer:
                    self.relocated_position = sprite.rect.topleft - self.relocation
                    self.display_surface.blit(sprite.image, self.relocated_position)

                # if transition --> blit "e"
                if (sprite == player and player.transition_collision) or (player.noticed and not player.in_dialog):
                    # wenn collision mit transition_object          oder      wenn dialog verfuegbar
                    icon_position = player.rect.midtop - vector(self.icon_e_animation.image.get_width() / 2, self.icon_e_animation.image.get_height() + 10)
                    #               kopf des spieler   -                 frame_breite                    frame_hoehe                      + 10 ueberm spieler

                    self.display_surface.blit(self.icon_e_animation.image, icon_position - self.relocation)
                    #

                

    def sort_sprites(self):
        return sorted(self.sprites(), key=self.sprite_sort_key)

    def sprite_sort_key(self, sprite):
        return sprite.rect.centery
