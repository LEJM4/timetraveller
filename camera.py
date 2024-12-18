from settings import *
from objects import *
from dialog import DialogSprite
from geometrie import Circle

# sorgt fuer das zeichnen aller sprites

class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.relocation = vector()
        self.display_surface = pygame.display.get_surface()

        self.icon_frames = {'icon_e_frames': [import_image('graphics', 'ui', 'e_button_icon_0'), import_image('graphics', 'ui', 'e_button_icon_1')],
                            'icon_space_frames': [import_image('graphics', 'ui', 'space_button_icon_0'), import_image('graphics', 'ui', 'space_button_icon_1')],
                            'icon_q_frames': [import_image('graphics', 'ui', 'q_button_icon_0'), import_image('graphics', 'ui', 'q_button_icon_1')]
                            }

        self.icon_e_animation = AnimatedSprites(
            pos=(0, 0),  # position wird spaeter angepasst
            frame_list=self.icon_frames['icon_e_frames'],
            groups=[],  # keine gruppen erforderlich, da  blit verwendet wird
            animation_speed=1.2  # geschwindigkeit der animation
        )
        self.icon_space_animation = AnimatedSprites(
            pos=(0, 0),  # position wird spaeter angepasst
            frame_list=self.icon_frames['icon_space_frames'],
            groups=[],  # keine gruppen erforderlich, da  blit verwendet wird
            animation_speed=1.2  # geschwindigkeit der animation
        )

        self.icon_q_animation = AnimatedSprites(
            pos=(0, 0),  # position wird spaeter angepasst
            frame_list= self.icon_frames['icon_q_frames'],
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
        self.icon_q_animation.frames = [pygame.transform.scale(frame, (player_width, frame.get_height())) for frame in self.icon_q_animation.frames] 
        self.icon_space_animation.frames = [pygame.transform.scale(frame, (player_width, frame.get_height())) for frame in self.icon_space_animation.frames] 
        #skaliert alle frames in der  liste --> oben
        self.icon_e_animation.update(dt) 
        self.icon_q_animation.update(dt) 
        self.icon_space_animation.update(dt) 
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
                
                #if bush collision
                if  (sprite == player and player.interaction_objects_collide):
                    icon_position = player.rect.midtop - vector(self.icon_q_animation.image.get_width() / 2, self.icon_q_animation.image.get_height() + 10)
                    #               kopf des spieler   -                 frame_breite                    frame_hoehe                      + 10 ueberm spieler
                    self.display_surface.blit(self.icon_q_animation.image, icon_position - self.relocation)
                
                if player.in_dialog:
                    icon_position = player.rect.midtop - vector(self.icon_space_animation.image.get_width() / 2, self.icon_space_animation.image.get_height() + 10)
                    #               kopf des spieler   -                 frame_breite                    frame_hoehe                      + 10 ueberm spieler
                    self.display_surface.blit(self.icon_space_animation.image, icon_position - self.relocation)
                    


                

    def sort_sprites(self):
        return sorted(self.sprites(), key=self.sprite_sort_key)

    def sprite_sort_key(self, sprite):
        return sprite.rect.centery
