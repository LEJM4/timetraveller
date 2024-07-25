from settings import *
from support import *
from timer import Timer
from random import randint
from math import sin
from game_data import *
from data import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, groups,	facing_direction, obstacle_objects, data, path, speed = 100):
        super().__init__(groups)

        #GAME-SETTINGS
        #status
        self.status = 'move'
        self.direction = vector()
        self.timers = {'hit_timer':    Timer(duration= 400,
                                            repeat = False,
                                            autostart= False,
                                            func = self.reset_vulnerability)}
        
        # 
        self.path = path

        # graphic
        self.import_pictures_4_animation()
        self.facing_direction = facing_direction
        self.frame_index = 0
        self.animation_speed = 10
        self.z_layer = LAYERS['main']


        #imports
        self.data = data

        # general setup
        #self.image = self.animations[self.facing_direction][self.frame_index]
        self.image =  self.frames[self.status][self.facing_direction][int(self.frame_index)]
        #self.image = self.status[self.get_state()][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.mask = pygame.mask.from_surface(self.image)
        



        # entity attributes
        self.pos = vector(self.rect.center)
        self.speed = speed

        self.blocked = False


        # collision
        self.hitbox_player = self.rect

        #Parametergroups
        self.obstacle_objects = obstacle_objects

        #weapons
        self.current_wepon = None



        #states
        #moving
        self.moving = False

        #attack
        self.attacking = False

        #collect
        self.collecting = False

        #bool
        self.is_vulnerable = True
	
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
        if self.current_wepon == 'pistol':    
            if int(self.frame_index) == 1 and self.attacking and not self.projectile_shot:
                
                match self.facing_direction:
                    case 'left': projectile_start_pos = self.rect.center + self.projectile_direction * (self.rect.width //2.4)
                    case 'right': projectile_start_pos = self.rect.center + self.projectile_direction * (self.rect.width //2.37)
                    case 'up': projectile_start_pos = self.rect.center + self.projectile_direction * (self.rect.width //2)
                    case 'down': projectile_start_pos = self.rect.center + self.projectile_direction * (self.rect.width //2)

                     

                
                self.create_star_projectile(projectile_start_pos, self.projectile_direction)
                self.projectile_shot = True

            
        
        if self.frame_index >= len(self.frames[self.status][self.facing_direction]):
            self.frame_index = 0

            if self.attacking:
                self.attacking = False
            
            if self.collecting:
                self.collecting = False
        

        self.image = self.frames[self.status][self.facing_direction][int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)

    def damage(self, weapon: str):
        if self.is_vulnerable:
            LIFE_DATA[self.entity_id]['health'] -= weapon_dict[weapon]
            self.is_vulnerable = False
            self.timers['hit_timer'].activate()
        print(self.is_vulnerable)
    
    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return True
        else:
            return False
    def blink_mask(self):
        if not self.is_vulnerable:
            if self.wave_value():
                mask = pygame.mask.from_surface(self.image)
                white_surf = mask.to_surface()
                white_surf.set_colorkey((0,0,0)) #entfernt all schwarzen pixel von der maske --> maske ist schwarz und weiss 
                self.image = white_surf

    def check_death(self):
        if LIFE_DATA[self.entity_id]['health'] <= 0:
             player_inventory['corps'] += 1
             self.kill()

    def reset_vulnerability(self):
        self.is_vulnerable = True
        print('timer works')
        print(self.is_vulnerable)

    def update_timer(self):
        for timer in self.timers.values():
            timer.update()

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


"""

class Character(Entity):
	def __init__(self, pos, frames, groups, facing_direction, character_data, player, create_dialog, collision_sprites, radius):
		super().__init__(pos, frames, groups, facing_direction)
		self.character_data = character_data
		self.player = player
		self.create_dialog = create_dialog
		self.collision_rects = [sprite.rect for sprite in collision_sprites if sprite is not self]

		# movement 
		self.has_moved = False
		self.can_rotate = True
		self.has_noticed = False
		self.radius = int(radius)
		self.view_directions = character_data['directions']

		self.timers = {
			'look around': Timer(1500, autostart = True, repeat = True, func = self.random_view_direction),
			'notice': Timer(500, func = self.start_move)
		}

	def random_view_direction(self):
		if self.can_rotate:
			self.facing_direction = choice(self.view_directions)

	def get_dialog(self):
		return self.character_data['dialog'][f'{'defeated' if self.character_data['defeated'] else 'default'}']

	def raycast(self):
		if check_connections(self.radius, self, self.player) and self.has_los() and not self.has_moved and not self.has_noticed:
			self.player.block()
			self.player.change_facing_direction(self.rect.center)
			self.timers['notice'].activate()
			self.can_rotate = False
			self.has_noticed = True
			self.player.noticed = True

	def has_los(self):
		if vector(self.rect.center).distance_to(self.player.rect.center) < self.radius:
			collisions = [bool(rect.clipline(self.rect.center, self.player.rect.center)) for rect in self.collision_rects]
			return not any(collisions)

	def start_move(self):
		relation = (vector(self.player.rect.center) - vector(self.rect.center)).normalize()
		self.direction = vector(round(relation.x), round(relation.y))

	def move(self, dt):
		if not self.has_moved and self.direction:
			if not self.hitbox.inflate(10,10).colliderect(self.player.hitbox):
				self.rect.center += self.direction * self.speed * dt
				self.hitbox.center = self.rect.center
			else:
				self.direction = vector()
				self.has_moved = True
				self.create_dialog(self)
				self.player.noticed = False

	def update(self, dt):
		for timer in self.timers.values():
			timer.update()

		self.animate(dt)
		if self.character_data['look_around']:
			self.raycast()
			self.move(dt)

            
"""