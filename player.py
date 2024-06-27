import pygame
from settings import *
from support import *
from entity import Entity_M


class Player(Entity_M):

	def __init__(self, pos, groups, status, obstacle_objects, interaction_objects, trail, data, path, create_star_bullet):
		super().__init__( pos, groups, status, obstacle_objects, data, path)

		
		#Parametergroups
		self.interaction_objects = interaction_objects
		self.trail = trail

		#
		self.create_star_projectile = create_star_bullet
		self.projectile_shot = 	False


		#collect

		self.collecting = False




		

	def input(self):
		keys = pygame.key.get_pressed()

		#moving
		if not self.attacking and not self.collecting:
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
				self.attacking = True
				self.direction = vector(0,0) #er bewegt sich nicht mehr --> er bleibt auf der Stelle stehen
				self.frame_index = 0
				self.projectile_shot = False
				#self.create_star_bullet(self.rect.center, vector(1,0))
				match self.status.split('_')[0]:
					case 'left': self.projectile_direction = vector (-1,0)
					case 'right': self.projectile_direction = vector (1,0)
					case 'up': self.projectile_direction = vector (0,-1)
					case 'down': self.projectile_direction = vector (0,1)
				

			#collect
			if keys[pygame.K_e]:
				self.collecting = True
				self.direction = vector(0,0) #er bewegt sich nicht mehr --> er bleibt auf der Stelle stehen
				self.frame_index = 0
				#self.status = 'up_collect'


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

		#print(self.status)


		

	def animation_player(self,dt):
		current_animation = self.animations[self.status]

		self.frame_index += self.anmation_speed * dt



		if int(self.frame_index) == 1 and self.attacking and not self.projectile_shot:
			

			projectile_start_pos = self.rect.center + self.projectile_direction * (self.rect.width // 50)

			#projectile_start_pos = self.rect.center + self.projectile_direction * 80
			
			self.create_star_projectile(projectile_start_pos, self.projectile_direction)
			self.projectile_shot = True
			#pass
			
		
		if self.frame_index >= len(current_animation):
			self.frame_index = 0

			if self.attacking:
				self.attacking = False
			
			if self.collecting:
				self.collecting = False

		self.image = current_animation[int(self.frame_index)]




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
		# self.block()
		# self.unblock()
		self.animation_player(dt) #animation in dt
		self.trail_collision()
