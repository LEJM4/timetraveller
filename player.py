import pygame
from settings import *
from support import *


class Player(pygame.sprite.Sprite):

	def __init__(self, pos, groups,	obstacle_objects, interaction_objects, trail, data, path):
		super().__init__(groups)

		# 
		self.path = path

		# graphic
		self.import_pictures_4_animation()
		self.status = 'down_idle'
		self.frame_index = 0
		self.anmation_speed = 10
		self.z_layer = LAYERS['main']


		#imports
		self.data = data

		# general setup
		self.image = self.animations[self.status][self.frame_index]
		self.rect = self.image.get_rect(center = pos)



		# movement attributes
		self.direction = pygame.math.Vector2()
		self.pos = pygame.math.Vector2(self.rect.center)
		self.change_speed = False
		self.speed = 100



		# collision
		self.hitbox_player = self.rect
		self.player_mask = pygame.mask.from_surface(self.image)

		#Parametergroups
		self.obstacle_objects = obstacle_objects
		self.interaction_objects = interaction_objects
		self.trail = trail



		#attack
		self.attacking = False


		#collect

		self.collecting = False

	
	def import_pictures_4_animation(self):
		# alle animaatonen mithiilfe der funktiion "subfolder" laden
		self.animations = import_sub_folders(*self.path)




	def animation_player(self,dt):
		current_animation = self.animations[self.status]

		self.frame_index += self.anmation_speed * dt
		if self.frame_index >= len(current_animation):
			self.frame_index = 0
			if self.attacking:
				self.attacking = False
			
			if self.collecting:
				self.collecting = False

		self.image = current_animation[int(self.frame_index)]
		

	def input(self):
		keys = pygame.key.get_pressed()

		#moving
		if not self.attacking:
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

		
		#attack
		if keys[pygame.K_SPACE]:
			self.attack = True
			self.direction = vector(0,0) #er bewegt sich nicht mehr --> er bleibt auf der Stelle stehen
			self.frame_index = 0

		#collect
		if keys[pygame.K_e]:
			self.collecting = True
			self.direction = vector(0,0) #er bewegt sich nicht mehr --> er bleibt auf der Stelle stehen
			self.frame_index = 0
			self.status = 'up_collect'


	def status_player(self):

		# idle 
		if self.direction.x == 0 and self.direction.y == 0:
			self.status = self.status.split('_')[0] + '_idle'

		#attack
		if self.attacking:
			self.status = self.status.split('_')[0] + '_attack'


		# collect
		if self.collecting:
			self.status = self.status.split('_')[0] + '_collect'

				

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
				self.speed = 200
				self.change_speed = True
				break
			else:
				self.speed = 100
				self.change_speed = False

	def update(self, dt): #update Methode in pygame --> verwendung mit 'pygame.time.Clock() --> aktualisiert SPiel
		self.input() #player input --> movement
		self.status_player() #status (idle or item use)
		self.move(dt) #movement in dt
		self.animation_player(dt) #animation in dt
		self.trail_collision()
