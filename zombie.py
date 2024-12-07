from settings import *
from entity import Entity
from timer import Timer
from random import randint
from game_data import *
import pygame
class Zombie:                                            
    def check_distance(self, radius, tolerance = 30):
        distance_vector = (vector(self.player.rect.center) - vector(self.rect.center)) 
        self.distance_squared = distance_vector.length_squared()
        radius_squared = radius**2
        return self.distance_squared < radius_squared

    def set_random_target(self):
        random_x = randint(-1000, 1000)
        random_y = randint(-1000, 1000)
        self.target_pos = vector(self.rect.center) + vector(random_x, random_y)
        #print('new target')

    def walk_around(self):
        self.timers['look_around'].activate() 
        
        PATH_LENGTH = 50 ** 2
        if not self.target_pos:
            self.set_random_target()
        #a = (self.pos - self.target_pos).length_squared() - (self.last_pos) 
        #print(a)
        if (self.pos - self.target_pos).length_squared() - (self.last_pos) == 0:
            self.set_random_target()
        
        direction = (vector(self.target_pos) - vector(self.rect.center))
        if direction.length() > 0:
            direction = direction.normalize()

        self.direction = direction

        if (self.target_pos - vector(self.rect.center)).length_squared() < PATH_LENGTH:
            self.set_random_target()
        self.last_pos = ((self.pos - self.target_pos).length_squared())

    def walk_around_2(self):
        self.timers['look_around'].activate() 
        if self.status == 'idle': 
            random_x = randint(-100, 100)
            random_y = randint(-100, 100)
        current_pos = vector(self.rect.center)
        random_pos = vector(self.rect.x + random_x  , y=self.rect.y + random_y)
        direction = (current_pos - random_pos).normalize()
        timer = self.timers['walk_around']
        if timer:
            self.direction = direction


    def get_player_direction(self):
        enemy_pos = vector(self.rect.center)
        player_pos = vector(self.player.rect.center)

        if self.distance_squared != 0: direction = (player_pos - enemy_pos).normalize()
#normalize(): returns a vector with the same direction but length 1 (https://pyga.me/docs/ref/math.html#pygame.math.Vector2.normalize)
        else: direction = vector(0,0)

        return(direction)
    
    def chase_player(self):
        self.direction = self.get_player_direction()
        

    def face_player(self):
        direction = self.get_player_direction()
        self.direction = vector()
        if -0.5 < direction.y < 0.5 :
            if direction.x < 0:
                self.facing_direction = 'left'
            elif direction.x > 0:
                self.facing_direction = 'right'
        else:
            if direction.y < 0:
                self.facing_direction = 'up'
            elif direction.y > 0:
                self.facing_direction = 'down'


class Zombie_1(Entity, Zombie):
    def __init__(self, pos, groups, frames, facing_direction, obstacle_objects, data, player, id):
        super().__init__(pos, groups, frames, facing_direction, obstacle_objects, data, speed= 200)
        
        #OVERWRITES
        self.projectile = False
        self.entity_id = id
        self.health = LIFE_DATA[id]['health']
        self.current_wepon = 'hand'
        self.animation_speed = 4

        
        self.last_pos = 0.0


        #timers
        self.timers = {'walk_around': Timer(duration=  randint(3000,7000),
                                            repeat = False,
                                            autostart= False,
                                            func = self.set_random_target()),
                        'look_around': Timer(duration=  randint(2000,7000),
                                            repeat = True,
                                            autostart= True,
                                            func =None),
                        'hit_timer':    Timer(duration= 2,
                                            repeat = False,
                                            autostart= False,
                                            func = self.reset_vulnerability)}

        self.player = player
        self.notice_radius = 400
        self.walk_radius = 300
        self.attack_radius = 50


        self.chase = False

        #print(self.distance)
        self.target_pos =  None
        self.distance_squared = 1

    
    def attack(self):
        self.attacking = True
        #print('the monster has attacked')


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

        #attack
        if self.attacking:
            self.status = 'attack'


           
        if self.check_distance(self.notice_radius):
            self.face_player()
            if self.check_distance(self.walk_radius):
                self.chase_player() 
                if self.check_distance(self.attack_radius):
                    self.attack()
        else:
            #self.status = 'idle'
            #self.direction = vector()
            self.walk_around()
        #print(self.status)

    def animation_leo(self, dt):
        self.frame_index += self.animation_speed * dt

        if int(self.frame_index) == 1 and self.attacking:
            if self.check_distance(self.attack_radius):
                self.player.damage(self.current_wepon)
                print(self.player.health)




        
        if self.frame_index >= len(self.frames[self.status][self.facing_direction]):
            self.frame_index = 0

            if self.attacking:
                self.attacking = False
            

        

        self.image = self.frames[self.status][self.facing_direction][int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt): #update Methode in pygame --> verwendung mit 'pygame.time.Clock() --> aktualisiert SPiel
        self.update_timer()
        self.update_status_and_facing_direction()

        self.move(dt) #movement in dt

        self.animation_leo(dt)
        self.blink_mask()

        self.check_death()



class Zombie_2(Entity, Zombie):
    def __init__(self, pos, groups, frames, facing_direction, obstacle_objects, data, player, create_projectile, id):
        super().__init__(pos, groups, frames, facing_direction, obstacle_objects, data, speed= 200)
        
        #OVERWRITES
        self.projectile = False
        self.health = hit_points['zombie_2']
        self.current_weapon = 'pistol'
        self.animation_speed = 4

        self.create_star_projectile = create_projectile


        self.last_pos = 0.0
        self.entity_id = id

        #timers
        self.timers = {'walk_around': Timer(duration=  randint(3000,7000),
                                            repeat = True,
                                            autostart= True,
                                            func =None),
                        'look_around': Timer(duration=  randint(2000,7000),
                                            repeat = True,
                                            autostart= True,
                                            func =None),
                        'hit_timer':    Timer(duration= 2,
                                            repeat = False,
                                            autostart= False,
                                            func = self.reset_vulnerability)}

        self.player = player
        self.notice_radius = 500
        self.walk_radius = 400
        self.attack_radius = 300

        self.projectile_shot = 	False

        self.chase = False

        #print(self.distance)
        self.target_pos =  None
        self.distance_squared = 1
        
    def attack(self):
        self.attacking = True
        self.projectile_shot = False

        #print('the monster has attacked')


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

        #attack
        if self.attacking:
            self.status = 'attack'


           
        if self.check_distance(self.notice_radius):
            self.face_player()
            if self.check_distance(self.walk_radius) and not self.check_distance(self.attack_radius):
                self.chase_player()
            if self.check_distance(self.attack_radius):
                self.attack()
        else:
            #self.status = 'idle'
            #self.direction = vector()
            self.walk_around()
        #print(self.status)


    def animation_leo(self, dt):

        self.frame_index += self.animation_speed * dt
        if self.current_weapon == 'pistol':    
            if int(self.frame_index) == 1 and self.attacking and not self.projectile_shot:
                self.projectile_direction = self.get_player_direction()
                

                projectile_start_pos = self.rect.center + self.projectile_direction * (self.rect.width // 1.5)
                projectile_start_pos = self.rect.center + self.projectile_direction * (self.rect.width // 1.05)

                
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
        self.update_timer()
        self.update_status_and_facing_direction()

        self.move(dt) #movement in dt

        self.animation_leo(dt)
        self.blink_mask()

        self.check_death()