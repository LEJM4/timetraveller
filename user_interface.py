from settings import *
from support import *

class Overlay:
	def __init__(self,player):
		self.player = player
		self.display_surface = pygame.display.get_surface()
		self.full_heart = import_image('graphics', 'ui', 'full_heart')
		self.half_heart = import_image('graphics', 'ui', 'half_heart')
		self.empty_heart = import_image('graphics', 'ui', 'empty_heart')
		#pygame.transform.scale(self.health_surf,)

	def display(self):
		for heart in range(hit_points['player']):
			x = SCREEN_WIDTH - (SCREEN_WIDTH// 20) - heart * (self.full_heart.get_width() + 4)
			y = 10
			self.display_surface.blit(self.empty_heart,(x,y))


		for heart in range(self.player.health):
			x = SCREEN_WIDTH - (SCREEN_WIDTH// 20) - heart * (self.full_heart.get_width() + 4)
			y = 10
			self.display_surface.blit(self.full_heart,(x,y))


"""
# falls der spieler die lebensanzeige ueber seinem kopf haben soll, dann diesen code nutzen
class Overlay:
    def __init__(self, player, camera):
        self.player = player
        self.camera = camera
        self.display_surface = pygame.display.get_surface()
        self.health_surf = import_image('graphics', 'ui', 'full_heart')

        # scaled hearts
        self.heart_width = self.health_surf.get_width() // 2  # haelfte breite
        self.heart_height = self.health_surf.get_height() // 2  # healfte hoehe
        self.health_surf = pygame.transform.scale(self.health_surf, (self.heart_width, self.heart_height))
        #bild skalieren

    def display(self):     
        for heart in range(self.player.health):
            x = self.player.rect.centerx - (self.player.health * (self.health_surf.get_width() + 4) / 2) + heart * (self.health_surf.get_width() + 4)
            
            y = self.player.rect.top - self.health_surf.get_height() - 5
            #   kopf von player     -      groesse von herz           - 5 (sicherheitsabstand)

            # move heart pos 
            x -= self.camera.relocation.x
            y -= self.camera.relocation.y

            self.display_surface.blit(self.health_surf, (x, y))
#"""

"""

pygame.init()
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ui = UserInterface(display_surface, 'lvl_1')


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit
        display_surface.fill((2,0,100))
        ui.display()
        pygame.display.update()
#"""