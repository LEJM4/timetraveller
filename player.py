import pygame
from settings import *
from support import *


class Player(pygame.sprite.Sprite):

	def __init__(self, pos, groups,	obstacle_objects, interaction_objects, trail, data):
		super().__init__(groups)
		self.animation_pictures()
		self.status = 'down_idle'
		self.frame_index = 0

		self.data = data
		self.z_layer = LAYERS['main']

		# general setup
		self.image = self.animations[self.status][self.frame_index]
		self.rect = self.image.get_rect(center = pos)



		# movement attributes
		self.direction = pygame.math.Vector2()
		self.pos = pygame.math.Vector2(self.rect.center)
		
		self.speed = 200



		# collision
		self.hitbox_player = self.rect
		self.player_mask = pygame.mask.from_surface(self.image)

		#Parametergroups
		self.obstacle_objects = obstacle_objects
		self.interaction_objects = interaction_objects
		self.trail = trail

	def animation_pictures(self):
		# Erzeugt ein Dict. mit versch. Animationen als Schlüssel + leere list --> als Werte
		self.animations = {
			'up': [], 'down': [], 'left': [], 'right': [], 
			'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
		}

		for animation_picture in self.animations.keys():
			#  Pfad zur Animation
			full_path = 'graphics/character/' + animation_picture

			# Bilder aus Ordner import.
			# importierte Bilder speichern als Liste Schlüssel des dict.
			self.animations[animation_picture] = import_folder(full_path)
			#folge daraus --> animationen der jeweiligen Aktivität des Characters


	def animation_player(self,dt):
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



	def status_player(self):
		#keys = pygame.key.get_pressed()
		
		# idle
		if self.direction.magnitude() == 0:
			self.status = self.status.split('_')[0] + '_idle'
		
		#pic item
		# if keys[pygame.K_e]:
		# 	if self.direction.magnitude() == 0: #ueberprueft die Laenge des Vektors
		# 		self.collision_bush()

		

				

	def move(self,dt):
		# vector normalisieren
		if self.direction.magnitude() > 0:
			self.direction = self.direction.normalize()

		# x movement
		self.pos.x += self.direction.x * self.speed * dt
		self.rect.centerx = self.pos.x
		self.obstacle_collision('horizontal')

		# y movement
		self.pos.y += self.direction.y * self.speed * dt
		self.rect.centery = self.pos.y
		self.obstacle_collision('vertical')
		

	def obstacle_collision(self, direction):
		for obstacle in self.obstacle_objects.sprites():
			if obstacle.hitbox.colliderect(self.hitbox_player):

				if direction == 'horizontal':
					if self.direction.x < 0:
						self.hitbox_player.left = obstacle.hitbox.right

					if self.direction.x > 0:
						self.hitbox_player.right = obstacle.hitbox.left

					self.rect.centerx = self.hitbox_player.centerx
					self.pos.x = self.hitbox_player.centerx
				
				else:
					if self.direction.y < 0:
						self.hitbox_player.top = obstacle.hitbox.bottom
					
					if self.direction.y > 0:
						self.hitbox_player.bottom = obstacle.hitbox.top
						
					self.rect.centery = self.hitbox_player.centery
					self.pos.y = self.hitbox_player.centery

	def collision_bush_update(self, type):
		
		if type == 'blueberry':
			self.data.blueberry += 1


		if type == 'raspberry':
			self.data.raspberry += 1

		if type == 'coin':
			self.data.coin += 1
	
	
	def trail_collision(self):
		for trail in self.trail.sprites():
			if trail.hitbox.colliderect(self.hitbox_player):
				self.speed = 900
			else:
				self.speed = 600
				pass
			








	def limit_movement(self):
		if self.rect.left < 640:  #limitiert Bewegung auf 3840 x --> nach links
			self.pos.x = 640 + self.rect.width / 2
			self.rect.left = 640
			self.hitbox_player.left = 640
		if self.rect.right > 3840: #limitiert Bewegung auf 3840 x --> nach rechts
			self.pos.x = 3840 - self.rect.width / 2
			self.rect.right = 3840
			self.hitbox_player.right = 3840
		if self.rect.bottom > 3200: #limitiert Bewegung auf 3520 y  --> nach unten
			self.pos.y = 3200 - self.rect.height / 2
			self.hitbox_player.centery = self.rect.centery
			self.rect.bottom = 3200
		if self.rect.top < 360: #limitiert Bewegung auf 360 y --> nach oben
			self.pos.y = 360 + self.rect.height / 2
			self.hitbox_player.centery = self.rect.centery
			self.rect.top = 360

	

	def update(self, dt): #update Methode in pygame --> verwendung mit 'pygame.time.Clock() --> aktualisiert SPiel
		self.input() #player input --> movement
		self.status_player() #status (idle or item use)
		self.move(dt) #movement in dt
		self.animation_player(dt) #animation in dt
		self.limit_movement()
		#self.collision_bush_update() #--> nur zum ueberpruefen aufrufen
		self.trail_collision()