from settings import *
from support import *
from game_data import *

# zeigt leben (oben rechts in der ecke) an

class Overlay:
	def __init__(self):
		self.health = LIFE_DATA['player']['health']
		self.screen = pygame.display.get_surface() 
		self.full_heart = import_image('graphics', 'ui', 'full_heart') # import der bilder
		self.half_heart = import_image('graphics', 'ui', 'half_heart') # import der bilder
		self.empty_heart = import_image('graphics', 'ui', 'empty_heart') # import der bilder
		#pygame.transform.scale(self.health_surf,)

	def display(self): 
		for empty_heart in range(self.health): # fuer jedes herz
			x = SCREEN_WIDTH - (SCREEN_WIDTH// 20) - empty_heart * (self.full_heart.get_width() + 4) # berechnung der position x
			y = SCREEN_HEIGHT // 80 # berechnung der position y
			self.screen.blit(self.empty_heart,(x,y)) # auf screen zeigen


		for heart in range(LIFE_DATA['player']['health']):
			x = SCREEN_WIDTH - (SCREEN_WIDTH// 20) - heart * (self.full_heart.get_width() + 4) # berechnung der position x
			y = SCREEN_HEIGHT // 80 # berechnung der position y
			self.screen.blit(self.full_heart,(x,y)) # auf screen zeigen

