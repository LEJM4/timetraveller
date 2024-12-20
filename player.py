import pygame
from settings import *
from support import *
from entity import Entity
from data import *

# class player nutzt sehr viel von entity
 
class Player(Entity):

	def __init__(self, pos, groups, frames, facing_direction, obstacle_objects, interaction_objects, trail, data, id, create_projectile):
		super().__init__(pos, groups, frames, facing_direction, obstacle_objects, data)
		
        #OVERWRITES
		self.current_wepon = 'pistol'

		
		self.entity_id = id
		self.speed = 300


		
		#Parametergroups
		self.interaction_objects = interaction_objects
		self.interaction_objects_collide = False
		self.trail = trail

		#
		self.create_star_projectile = create_projectile
		self.projectile_shot = 	False
		self.transition_collision = False

		self.in_dialog = False
		self.noticed = False


	def input(self):
		keys = pygame.key.get_pressed()

		#moving
		if not self.attacking and not self.collecting:
			if keys[pygame.K_UP] or keys[pygame.K_w]:
				self.direction.y = -1
				#self.facing_direction = 'up'
			elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
				self.direction.y = 1
				#self.facing_direction = 'down'
			else:
				self.direction.y = 0

			if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
				self.direction.x = 1
				#self.facing_direction = 'right'
			elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
				self.direction.x = -1
				#self.facing_direction = 'left'
			else:
				self.direction.x = 0

		
			#attack
			if keys[pygame.K_SPACE]:
				self.attack()

			#collect
			if keys[pygame.K_q]:
				self.collecting = True
				self.direction = vector(0,0) #er bewegt sich nicht mehr --> er bleibt auf der Stelle stehen
				self.frame_index = 0
				#self.status = 'up_collect'

	def attack(self):
		self.attacking = True
		self.direction = vector(0,0) #er bewegt sich nicht mehr --> er bleibt auf der Stelle stehen
		self.frame_index = 0
		self.projectile_shot = False
		match self.facing_direction:
			case 'left': self.projectile_direction = vector (-1,0)
			case 'right': self.projectile_direction = vector (1,0)
			case 'up': self.projectile_direction = vector (0,-1)
			case 'down': self.projectile_direction = vector (0,1)


	def animation_leo(self, dt):

		self.frame_index += self.animation_speed * dt
		if self.current_wepon == 'pistol':    
			if int(self.frame_index) == 1 and self.attacking and not self.projectile_shot:
				
				match self.facing_direction:
					case 'left': projectile_start_pos = self.rect.center + self.projectile_direction * (self.rect.width //2.4)
					case 'right': projectile_start_pos = self.rect.center + self.projectile_direction * (self.rect.width //2.37)
					case 'up': projectile_start_pos = self.rect.center + self.projectile_direction * (self.rect.width // 1.5)
					case 'down': projectile_start_pos = self.rect.center + self.projectile_direction * (self.rect.width //2)

						
				self.create_star_projectile(projectile_start_pos, self.projectile_direction, self.facing_direction)
				self.projectile_shot = True

			
		
		if self.frame_index >= len(self.frames[self.status][self.facing_direction]):
			self.frame_index = 0

			if self.attacking:
				self.attacking = False
			
			if self.collecting:
				self.collecting = False
		

		self.image = self.frames[self.status][self.facing_direction][int(self.frame_index)]
		self.mask = pygame.mask.from_surface(self.image)

	def update(self, dt): #update Methode in pygame --> verwendung mit 'pygame.time.Clock() --> aktualisiert SPiel
		if not self.blocked:
			self.input() #player input --> movement
			self.update_status_and_facing_direction() 
			self.move(dt) #movement in dt
			# self.block()
			# self.unblock()
		self.update_timer()
		self.animation_leo(dt)
		self.blink_mask()

		self.check_death()
