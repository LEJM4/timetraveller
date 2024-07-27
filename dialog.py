from settings import *
from timer import Timer

class Robo(pygame.sprite.Sprite):
    def __init__(self, pos, groups, player, character_data, create_dialog, z_layer=LAYERS['water']):
        super().__init__(groups)
        self.player = player
        self.pos = pos
        self.z_layer = z_layer
        self.image = import_image('graphics', 'ui', 'full_heart')
        self.rect = self.image.get_rect(center = pos)
        self.notice_radius = 150
        self.character_data = character_data
        self.create_dialog = create_dialog
        # print(self.character_data)
        # print('robo ist da')

    def check_distance(self, radius, tolerance = 30):
        distance_vector = (vector(self.player.rect.center) - vector(self.rect.center)) 
        #distance_vector = vector vom spieler - vector vom zombie
        # moeglich waere auch:
        # distance_vector = (vector(self.player.rect.center) - vector(self.rect.center)).magnitude() 
        #magnitude : https://pyga.me/docs/ref/math.html#pygame.math.Vector2.magnitude
        # quadriert und zieht die Wurzel --> wurzel ziehen ist fuer computer bloed zu rechnen --> deshalb quadrieren
        # (Danke "dezer_ted")
        self.distance_squared = distance_vector.length_squared()
        radius_squared = radius**2
        return self.distance_squared < radius_squared
    
    def get_dialog(self):
        current_dialog_id = str(self.character_data['current_dialog'])
        return self.character_data['dialog'][current_dialog_id]

    def update(self, dt):
        keys = pygame.key.get_just_pressed() #ueberprueft
        if self.check_distance(self.notice_radius):
            if self.character_data['can_talk']:
                self.player.noticed = True #damit icon eingeblendet wird
                if keys[pygame.K_e]:
                    self.player.block()
                    self.create_dialog(self)
                    self.player.in_dialog = True #muss true sein damit in camera das icon nicht mehr angezeigt wird
                #self.player.noticed = False #muss hier nochmal falls weil ansonsten, wenn er einmal im radius war, wird icon dauerhaft angezeigt
            else:
                self.player.noticed = False
        else:
            self.player.noticed = False





class DialogTree:
    def __init__(self, object, player, all_sprites, font, end_dialog):
        self.player = player
        self.object = object
        print(self.object)
        self.end_dialog = end_dialog
        self.all_sprites = all_sprites,
        self.font = font
        self.dialog = object.get_dialog()
        self.dialog_num = len(self.dialog)
        self.dialog_index = 0

        self.current_dialog = DialogSprite(self.dialog[self.dialog_index], self.object, self.all_sprites, self.font)

        self.screen = pygame.display.get_surface()

        self.dialog_timer = Timer(500, autostart= True)

    
    def input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_SPACE] or keys[pygame.K_RETURN] and not self.dialog_timer.active: #prueft ob eingabe und timer
            self.current_dialog.kill() #entfernt den aktuellen dialog welcher mit dem index 0 --> oben --> erschaffen wurde
            self.dialog_index += 1 #dialog index erhoet
            if self.dialog_index < self.dialog_num: # wenn der index kleiner ist als die laenge aller verfuegbaren dialoge 
                self.current_dialog = DialogSprite(self.dialog[self.dialog_index], self.object, self.all_sprites, self.font) #neuer dialog mit neuen woertern
                self.dialog_timer.activate() #erschafft neuen timer
            else:
                self.end_dialog(self.object)

    def update(self):
        self.dialog_timer.update()
        self.input()

class DialogSprite(pygame.sprite.Sprite):
    def __init__(self, message, character, groups, font):
        super().__init__(groups)
        self.z_layer = LAYERS['dialog']
        self.screen = pygame.display.get_surface()

        self.screen_width, self.screen_height = self.screen.get_size()

		# text 
        text_surf = font.render(message, False, 'black')
        padding = 5
        width = max(30, text_surf.get_width() + padding * 2)
        height = text_surf.get_height() + padding * 2

        # background
        surf = pygame.Surface((width, height), pygame.SRCALPHA)
        surf.fill((0,0,0,0))
        pygame.draw.rect(surf, 'white', surf.get_frect(topleft = (0,0)),0, 4)
        surf.blit(text_surf, text_surf.get_frect(center = (width / 2, height / 2)))

        self.image = surf
        self.rect = self.image.get_frect(midbottom = character.rect.midtop + vector(0,-10))
        #clear code
