import pygame
from settings import *
from support import *


class Player(pygame.sprite.Sprite):

	def __init__(self, pos, group):
		super().__init__(group)
		self.import_assets()
		self.status = 'down_idle'
		self.frame_index = 0

		# general setup
		self.image = self.animations[self.status][self.frame_index]
		self.rect = self.image.get_rect(center = pos)


		# movement attributes
		self.direction = pygame.math.Vector2()
		self.pos = pygame.math.Vector2(self.rect.center)
		self.speed = 200



		# collision
		self.hitbox_player = self.rect
		#self.collision_sprites = collision_sprites

	def import_assets(self):
		# Erzeugt ein Dict. mit versch. Animationen als Schlüssel + leere list --> als Werte
		self.animations = {
			'up': [], 'down': [], 'left': [], 'right': [], 
			'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
		}

		for animation in self.animations.keys():
			#  Pfad zur Animation
			full_path = 'graphics/character/' + animation

			# Bilder aus Ordner import.
			# importierte Bilder speichern als Liste Schlüssel des dict.
			self.animations[animation] = import_folder(full_path)
			#folge daraus --> animationen der jeweiligen Aktivität des Characters


	def animate(self,dt):
		self.frame_index += 7 * dt #Zahl enspricht der schnelligkeit der Bilder fuer die Animation
		if self.frame_index >= len(self.animations[self.status]):
			self.frame_index = 0

		self.image = self.animations[self.status][int(self.frame_index)]

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_UP] or keys[pygame.K_w]:
			self.direction.y = -1
			self.status = 'up'
		elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
			self.direction.y = 1
			self.status = 'down'
		else:
			self.direction.y = 0

		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			self.direction.x = 1
			self.status = 'right'
		elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
			self.direction.x = -1
			self.status = 'left'
		else:
			self.direction.x = 0

	def get_status(self):
		keys = pygame.key.get_pressed()
		
		# idle
		if self.direction.magnitude() == 0:
			self.status = self.status.split('_')[0] + '_idle'
		
		#pic item
		if keys[pygame.K_e]:
			if self.direction.magnitude() == 0: #ueberprueft die Laenge des Vektors
				print("pick up an item")

		

				

	def move(self,dt):
		# vector normalisieren
		if self.direction.magnitude() > 0:
			self.direction = self.direction.normalize()

		# x movement
		self.pos.x += self.direction.x * self.speed * dt
		self.rect.centerx = self.pos.x

		# y movement
		self.pos.y += self.direction.y * self.speed * dt
		self.rect.centery = self.pos.y

	def limit_movement(self):
		if self.rect.left < 0:
			self.pos.x = 0 + self.rect.width / 2
			self.rect.left = 0
			self.hitbox_player.left = 0
		if self.rect.right > 1280:
			self.pos.x = 1280 - self.rect.width / 2
			self.rect.right = 1280
			self.hitbox_player.right = 1280
		if self.rect.bottom > 720:
			self.pos.y = 720 - self.rect.height / 2
			self.hitbox_player.centery = self.rect.centery
			self.rect.bottom = 720
		if self.rect.top < 0:
			self.pos.y = 0 + self.rect.height / 2
			self.hitbox_player.centery = self.rect.centery
			self.rect.top = 0
	

	def update(self, dt): #update Methode in pygame --> verwendung mit 'pygame.time.Clock() --> aktualisiert SPiel
		self.input() #player input --> movement
		self.get_status() #status (idle or item use)
		self.move(dt) #movement in dt
		self.animate(dt) #animation in dt
		self.limit_movement()