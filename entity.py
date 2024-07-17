from settings import *
from support import *
from timer import Timer
from random import randint

   
class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, groups,	facing_direction, obstacle_objects, data, path, speed = 100):
        super().__init__(groups)

        #status
        self.status = 'move'
		# 
        self.path = path

        # graphic
        self.import_pictures_4_animation()
        self.facing_direction = facing_direction
        self.frame_index = 0
        self.animation_speed = 10
        self.z_layer = LAYERS['main']

        self.direction = vector()

        #imports
        self.data = data

        # general setup
        #self.image = self.animations[self.facing_direction][self.frame_index]
        self.image =  self.frames[self.status][self.facing_direction][int(self.frame_index)]
        #self.image = self.status[self.get_state()][self.frame_index]
        self.rect = self.image.get_rect(center = pos)



        # movement attributes
        self.pos = vector(self.rect.center)
        self.change_speed = False
        self.speed = speed

        self.blocked = False


        # collision
        self.hitbox_player = self.rect
        self.player_mask = pygame.mask.from_surface(self.image)

        #Parametergroups
        self.obstacle_objects = obstacle_objects

        #weapons
        self.projectile = True
        #states
        #moving
        self.moving = False

        #attack
        self.attacking = False

        #collect
        self.collecting = False
	
    def import_pictures_4_animation(self):
        self.frames = import_multiple_spritesheets(4, 4, *self.path)

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


    def update_status_and_facing_direction(self):

        #idle / move
        
        moving = bool(self.direction)
        
        if moving:
            self.status = 'move'
            if self.direction.x != 0:
                self.facing_direction = 'right' if self.direction.x > 0 else 'left'
            if self.direction.y != 0:
                self.facing_direction = 'down' if self.direction.y > 0 else 'up'
        
        else:
            self.status = 'idle'
            """
            if self.facing_direction.endswith('_idle'): 
                self.facing_direction = self.facing_direction
            else:
                self.facing_direction += '_idle'
            """
        
        #attack
        if self.attacking:
            self.status = 'attack'
            self.facing_direction = self.facing_direction.replace('_idle', '')  # remove _idle if attacking

        #collect
        if self.collecting:
            self.status = 'collect'
            self.facing_direction = self.facing_direction.replace('_idle', '')  # remove _idle if collecting


        #return f"{self.facing_direction}{'' if moving else '_idle'}"



    def animation_leo(self, dt):

        self.frame_index += self.animation_speed * dt
        if self.projectile:    
            if int(self.frame_index) == 1 and self.attacking and not self.projectile_shot:
                

                projectile_start_pos = self.rect.center + self.projectile_direction * (self.rect.width // 50)

                
                self.create_star_projectile(projectile_start_pos, self.projectile_direction)
                self.projectile_shot = True

            
        
        if self.frame_index >= len(self.frames[self.status][self.facing_direction]):
            self.frame_index = 0

            if self.attacking:
                self.attacking = False
            
            if self.collecting:
                self.collecting = False
        

        self.image = self.frames[self.status][self.facing_direction][int(self.frame_index)]


    def block(self):
        self.blocked = True
        self.direction = vector(0,0)

    def unblock(self):
        self.blocked = False

    # def get_state(self):
    #     moving = bool(self.direction)
    #     if moving:
    #         if self.direction.x != 0:
    #             self.facing_direction = 'right' if self.direction.x > 0 else 'left'
    #         if self.direction.y != 0:
    #             self.facing_direction = 'down' if self.direction.y > 0 else 'up'

    #         return f'{self.facing_direction}{"" if moving else "_idle"}'
        
    #     elif self.collecting:
    #         return f'{self.facing_direction}_collect'
        
    #     elif self.attacking:
    #         return f'{self.facing_direction}_attack'







class Characters:
	def get_player_distance_direction(self):
		enemy_pos = self.rect.center
		player_pos = self.player.rect.center
		distance = vector(player_pos) - vector(enemy_pos).magnitude()
        
		if distance.length() != 0:
			direction = (player_pos - enemy_pos).normalize()
		else:
			direction = vector()

		return (distance, direction)

	def face_player(self):
		distance, direction = self.get_player_distance_direction()

		if distance < self.notice_radius:
			if -0.5 < direction.y < 0.5:
				if direction.x < 0: # player to the left
					self.status = 'left_idle'
				elif direction.x > 0: # player to the right
					self.status = 'right_idle'
			else:
				if direction.y < 0: # player to the top
					self.status = 'up_idle'
				elif direction.y > 0: # player to the bottom
					self.status = 'down_idle'

	def walk_to_player(self):
		distance, direction = self.get_player_distance_direction()
		if self.attack_radius < distance < self.walk_radius:
			self.direction = direction
			self.status = self.status.split('_')[0]
		else:
			self.direction = vector()
    