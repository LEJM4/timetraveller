import pygame
from settings import *
from support import *
from entity import Entity
from data import *

class Player(Entity):

	def __init__(self, pos, groups, facing_direction, obstacle_objects, interaction_objects, trail, data, path, id, create_projectile):
		super().__init__( pos, groups, facing_direction, obstacle_objects, data, path)
		
        #OVERWRITES
		self.health = hit_points['player']
		self.current_wepon = 'pistol'

		
		self.entity_id = id
		self.speed = 500

		
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

	def import_pictures_4_animation(self):
		#self.frames = import_multiple_spritesheets(8, 4, *self.path)
		#'''
		self.frames = {'attack': character_image_importer_vertical(4,4, 'graphics', 'player', 'attack'), #hendrik laesst mich nicht gut strukturierten und effizienten code schreiben
						'collect': character_image_importer_vertical(7,4, 'graphics', 'player', 'collect'), #hendrik laesst mich nicht gut strukturierten und effizienten code schreiben
						'idle': character_image_importer_vertical(1,4, 'graphics', 'player', 'idle'), #hendrik laesst mich nicht gut strukturierten und effizienten code schreiben
						'move': character_image_importer_vertical(8,4, 'graphics', 'player', 'move')} #hendrik laesst mich nicht gut strukturierten und effizienten code schreiben
		#'''

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
		#self.create_star_bullet(self.rect.center, vector(1,0))
		match self.facing_direction:
			case 'left': self.projectile_direction = vector (-1,0)
			case 'right': self.projectile_direction = vector (1,0)
			case 'up': self.projectile_direction = vector (0,-1)
			case 'down': self.projectile_direction = vector (0,1)

	
	






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
