from settings import *
from entity import Entity
from timer import Timer
from random import randint


class Zombie:                                            
    def check_distance(self, radius, tolerance = 30):
        distance_vector = (vector(self.player.rect.center) - vector(self.rect.center)) 
        #distance_vector = vector vom spieler - vector vom zombie
        # moeglich waere auch:
        # distance_vector = (vector(self.player.rect.center) - vector(self.rect.center)).magnitude() 
        #magnitude : https://pyga.me/docs/ref/math.html#pygame.math.Vector2.magnitude
        # quadriert und zieht die Wurzel --> wurzel ziehen ist fuer computer bloed zu rechnen --> deshalb quadrieren
        # (Danke "dezer_ted")
        self.distance_squared = distance_vector.length_squared()
        radius_squared = radius**2
        return self.distance_squared < radius_squared

    def set_random_target(self):
        random_x = randint(-100, 100)
        random_y = randint(-100, 100)
        target_pos = vector(self.rect.center) + vector(random_x, random_y)
        self.timers['walk_around'].activate() 
        return target_pos

    def walk_around(self):
        target_pos = self.set_random_target()
        direction = (vector(target_pos) - vector(self.rect.center)).normalize()
        if direction.length() > 0:
            direction = direction.normalize()
        timer = self.timers['walk_around']
        if target_pos == None: self.set_random_target()
        if timer:
            self.direction = direction
            if (target_pos - vector(self.rect.center)).length_squared() < 10**2:
                            target_pos = self.set_random_target()
        
        else:
             self.set_random_target()

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
    def __init__(self, pos, groups, facing_direction, obstacle_objects, data, path, player):
        super().__init__(pos, groups, facing_direction, obstacle_objects, data, path, speed= 200)
        
        #OVERWRITES
        self.projectile = False
        self.health = 3
        self.current_wepon = 'hand'


        #
        self.path = path

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
        self.walk_radius = 300
        self.attack_radius = 50


        self.chase = False

        #print(self.distance)
        self.target_pos =  None
        self.distance_squared = 1
        
    def import_pictures_4_animation(self):
        self.frames = import_multiple_spritesheets(4, 4, *self.path)
        ''' 
        self.frames = {'attack': character_image_importer(4,4, 'graphics', 'npc', 'npc_1', 'attack'), #hendrik laesst mich nicht gut strukturierten und effizienten code schreiben
                       'collect': character_image_importer(4,4, 'graphics', 'npc', 'npc_1', 'hendrik'), #hendrik laesst mich nicht gut strukturierten und effizienten code schreiben
                       'idle': character_image_importer(1,4, 'graphics', 'npc', 'npc_1', 'hendrik'), #hendrik laesst mich nicht gut strukturierten und effizienten code schreiben
                       'move': character_image_importer(4,4, 'graphics', 'npc', 'npc_1', 'hendrik')} #hendrik laesst mich nicht gut strukturierten und effizienten code schreiben
        #'''
    
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

    def update(self, dt): #update Methode in pygame --> verwendung mit 'pygame.time.Clock() --> aktualisiert SPiel
        self.update_timer()
        self.update_status_and_facing_direction()

        self.move(dt) #movement in dt

        self.animation_leo(dt)



class Zombie_2(Entity, Zombie):
    def __init__(self, pos, groups, facing_direction, obstacle_objects, data, path, player, create_projectile):
        super().__init__(pos, groups, facing_direction, obstacle_objects, data, path, speed= 200)
        
        #OVERWRITES
        self.projectile = False
        self.health = 3
        self.current_weapon = 'pistol'

        self.create_star_projectile = create_projectile


        #
        self.path = path

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
        
    def import_pictures_4_animation(self):
        self.frames = import_multiple_spritesheets(4, 4, *self.path)

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


    def update(self, dt): #update Methode in pygame --> verwendung mit 'pygame.time.Clock() --> aktualisiert SPiel
        self.update_timer()
        self.update_status_and_facing_direction()

        self.move(dt) #movement in dt

        self.animation_leo(dt)