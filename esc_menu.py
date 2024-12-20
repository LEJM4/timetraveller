import pygame
from settings import *
from button import Button
import time

# viel code und viele dinge
# buttons und ausrichtung ist skalierbar und passt sich der screen_size an

class EscMenu:
    def __init__(self, screen):#, game_state_manager):
        #state
        

        #
        self.last_click_time = 0
        self.click_delay = 100 #200 milisek. zwischen clicks

        self.screen = screen  
        self.esc_visible = False 

        #button_get_clicked_states
        self.resume_state = False

        #Options
        self.settings_state = False

        self.settings_audio = False
        self.settings_screen = False
        self.settings_back = False

        #exit
        self.button_pressed_exit = False

        #button_settings
        self.button_width = SCREEN_WIDTH / 4.5
        self.button_height = SCREEN_HEIGHT / 8


        total_height = (3 * self.button_height) + (2 * space_between_buttons_y)  #gesamthoehe der anordnung
        self.first_y = (SCREEN_HEIGHT / 2) - (total_height / 2)   # wo muss der erste button hin

        #button in center
        self.button_pos_x = SCREEN_WIDTH / 2 - self.button_width / 2 #berechnet die center position fuer x --> damit das Zentrum des Buttons bei x liegt
        self.button_pos_y = self.first_y - self.button_height / 2 #berechnet die center position fuer y --> damit das Zentrum des Buttons bei y liegt

    #first button screen: [Resume; Options; Exit]
    def normal_resume_options_exit(self):
        normal_resume_options_exit_list = []
        self.resume_button = Button(text= "RESUME", 
                                x_position=  self.button_pos_x, #pos x
                                y_position= self.button_pos_y, #erster button
                                button_width= self.button_width,
                                button_height= self.button_height,
                                screen= self.screen,
                                collision_allowed = True)
        
        self.settings_button = Button(text= "SETTINGS", 
                                x_position=  self.button_pos_x, #pos x
                                y_position= self.button_pos_y + self.button_height + space_between_buttons_y, #zweiter button
                                button_width= self.button_width,
                                button_height= self.button_height,
                                screen= self.screen,
                                collision_allowed = True)
        
        self.exit_button = Button(text= "HOME", 
                                x_position=  self.button_pos_x, #pos x
                                y_position= self.button_pos_y + 2* (self.button_height + space_between_buttons_y), # dritter button
                                button_width= self.button_width,
                                button_height= self.button_height,
                                screen= self.screen,
                                collision_allowed = True)
        

        normal_resume_options_exit_list.append(self.resume_button)
        normal_resume_options_exit_list.append(self.settings_button)
        normal_resume_options_exit_list.append(self.exit_button)

        for button in normal_resume_options_exit_list:
            button.draw(self.screen)
        
        if self.can_click() == True:
            if self.resume_button.button_is_pressed == True:
                self.esc_visible = False
                print('RESUME')
            
            if self.settings_button.button_is_pressed == True:
                self.esc_visible = False
                self.settings_state = True

            if self.exit_button.button_is_pressed == True:
                self.button_pressed_exit = True

    def settings(self):
        settings_audio_screen_back_list = []
        self.audio_button = Button(text= "AUDIO", 
                                x_position=  self.button_pos_x, #pos x
                                y_position= self.button_pos_y, #erster button
                                button_width= self.button_width,
                                button_height= self.button_height,
                                screen= self.screen,
                                collision_allowed = True)
        
        self.screen_button = Button(text= "SCREEN", 
                                x_position=  self.button_pos_x, #pos x
                                y_position= self.button_pos_y + self.button_height + space_between_buttons_y, #zweiter button
                                button_width= self.button_width,
                                button_height= self.button_height,
                                screen= self.screen,
                                collision_allowed = True)
        
        self.back_button = Button(text= "BACK", 
                                x_position=  self.button_pos_x, #pos x
                                y_position= self.button_pos_y + 2* (self.button_height + space_between_buttons_y), # dritter button
                                button_width= self.button_width,
                                button_height= self.button_height,
                                screen= self.screen,
                                collision_allowed = True)
        

        settings_audio_screen_back_list.append(self.audio_button)
        settings_audio_screen_back_list.append(self.screen_button)
        settings_audio_screen_back_list.append(self.back_button)

        for button in settings_audio_screen_back_list:
            button.draw(self.screen)

        if self.can_click():
            if self.audio_button.button_is_pressed == True:
                self.settings_state = False
                self.settings_audio = True
            
            if self.screen_button.button_is_pressed == True:
                self.settings_state = False
                self.settings_screen = True

            if self.back_button.button_is_pressed == True:
                self.settings_state = False
                time.sleep(0.1)
                self.esc_visible = True


    
    def settings_screen_button(self):
        screen_button_y = SCREEN_HEIGHT / 7
        screen_button_space_y = SCREEN_HEIGHT / 40

        screen_button_width_SCREEN = SCREEN_WIDTH / 2.5
        screen_button_x_pos_SCREEN = self.button_pos_x - int(screen_button_width_SCREEN// 4)
        
        
        screen_button_height = SCREEN_HEIGHT / 12


        screen_button_width_normal = SCREEN_WIDTH / 3.5
        screen_button_x_pos_normal = self.button_pos_x - int(screen_button_width_normal // 6)

        screen_button_height = SCREEN_HEIGHT / 12
        screen_button_list = []

        self.screen_button = Button(text= "SCREEN", 
                                x_position=  screen_button_x_pos_SCREEN, #pos x
                                y_position= screen_button_y , #erster button
                                button_width= screen_button_width_SCREEN,
                                button_height= screen_button_height,
                                screen= self.screen,
                                collision_allowed = False)        
        
        self.small_screen_setting_button = Button(text= "small: (800x600)", 
                                x_position=  screen_button_x_pos_normal, #pos x
                                y_position= screen_button_y + screen_button_height + screen_button_space_y, 
                                button_width= screen_button_width_normal,
                                button_height= screen_button_height,
                                screen= self.screen,
                                collision_allowed = True) 
        
        self.medium_screen_setting_button = Button(text= "medium: (1280x720)", 
                                x_position=  screen_button_x_pos_normal, #pos x
                                y_position= screen_button_y + 2*(screen_button_height + screen_button_space_y),  # dritter button
                                button_width= screen_button_width_normal,
                                button_height= screen_button_height,
                                screen= self.screen,
                                collision_allowed = True)

        self.large_screen_setting_button = Button(text= 'large: (1920x1080)', 
                                x_position=  screen_button_x_pos_normal, #pos x
                                y_position= screen_button_y + 3*(screen_button_height + screen_button_space_y),  # dritter button
                                button_width= screen_button_width_normal,
                                button_height= screen_button_height,
                                screen= self.screen,
                                collision_allowed = True)

        self.full_screen_setting_button = Button(text= 'FULLSCREEN', 
                                x_position=  screen_button_x_pos_normal, #pos x
                                y_position= screen_button_y + 4*(screen_button_height + screen_button_space_y),  # dritter button
                                button_width= screen_button_width_normal,
                                button_height= screen_button_height,
                                screen= self.screen,
                                collision_allowed = True)          

        self.back_screen_setting_button = Button(text= "BACK", 
                                x_position=  screen_button_x_pos_SCREEN, #pos x
                                y_position= screen_button_y + 5*(screen_button_height + screen_button_space_y),  # dritter button
                                button_width= screen_button_width_SCREEN,
                                button_height= screen_button_height,
                                screen= self.screen,
                                collision_allowed = True) 
                  
        screen_button_list.append(self.screen_button)
        screen_button_list.append(self.small_screen_setting_button)
        screen_button_list.append(self.medium_screen_setting_button)
        screen_button_list.append(self.large_screen_setting_button)
        screen_button_list.append(self.full_screen_setting_button)
        screen_button_list.append(self.back_screen_setting_button)

        for button in screen_button_list:
           button.draw(self.screen)

        if self.can_click():
            if self.small_screen_setting_button.button_is_pressed == True:
                new_SCREEN_WIDTH = 800
                new_SCREEN_HEIGHT = 600
                self.resolution_changed = True
                print(f'Aenderung der Bildschirmgroesse zu {800,600}')
                self.screen = pygame.display.set_mode((new_SCREEN_WIDTH, new_SCREEN_HEIGHT), pygame.FULLSCREEN)
                SCREEN_WIDTH = new_SCREEN_WIDTH
                SCREEN_HEIGHT = new_SCREEN_HEIGHT
                
            
            if self.medium_screen_setting_button.button_is_pressed == True:
                new_SCREEN_WIDTH = 1280
                new_SCREEN_HEIGHT = 720
                self.resolution_changed = True            
                print(f'Aenderung der Bildschirmgroesse zu {1280,720}')
                self.screen = pygame.display.set_mode((new_SCREEN_WIDTH, new_SCREEN_HEIGHT), pygame.FULLSCREEN)
                SCREEN_WIDTH = new_SCREEN_WIDTH
                SCREEN_HEIGHT = new_SCREEN_HEIGHT


            if self.large_screen_setting_button.button_is_pressed == True:
                new_SCREEN_WIDTH = 1920
                new_SCREEN_HEIGHT = 1080
                self.resolution_changed = True                
                print(f'Aenderung der Bildschirmgroesse zu {1920,1080}')
                self.screen = pygame.display.set_mode((new_SCREEN_WIDTH, new_SCREEN_HEIGHT), pygame.FULLSCREEN)
                SCREEN_WIDTH = new_SCREEN_WIDTH
                SCREEN_HEIGHT = new_SCREEN_HEIGHT

            if self.full_screen_setting_button.button_is_pressed == True:
                new_SCREEN_WIDTH = pygame.display.Info().current_w
                new_SCREEN_HEIGHT = pygame.display.Info().current_h
                self.resolution_changed = True
                print(f'Aenderung der Bildschirmgroesse zu FULLSCREEN')
                self.screen = pygame.display.set_mode((new_SCREEN_WIDTH, new_SCREEN_HEIGHT), pygame.FULLSCREEN)
                SCREEN_WIDTH = new_SCREEN_WIDTH
                SCREEN_HEIGHT = new_SCREEN_HEIGHT

            if self.back_screen_setting_button.button_is_pressed == True:
                self.settings_screen = False
                self.settings_state = True 

    def can_click(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_click_time >= self.click_delay:
            self.last_click_time = current_time
            return True
        return False
    
    def run(self):
        #esc

        if self.esc_visible == True:  # menu active?
            self.normal_resume_options_exit()

        #resume
        if self.resume_state == True:
            self.esc_visible = False

        #setting buttons
        if self.settings_state == True:
            self.settings()

        if self.settings_audio == True:
            self.esc_visible = False
            pass

        if self.settings_screen == True:
            self.esc_visible = False
            pass
         
        if self.button_pressed_exit == True:
            pass




    def check_4_esc_menu_active(self):
        self.resume_state = False
        #settings
        self.settings_state = False
        self.settings_audio = False
        self.settings_screen = False
        self.settings_back = False
        #exit
        self.button_pressed_exit = False
        self.esc_visible = True  # 
