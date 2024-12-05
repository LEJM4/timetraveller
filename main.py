from install_requirements import installieren_aller_requirements


#installieren_aller_requirements()

import pygame, sys
# from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from level import Level
from data import Data   
from esc_menu import EscMenu
from settings import *


class Game:
    def __init__(self):
        pygame.init() #initialisieren von Pygame

        self.mouse_visible = False #mouse unsichtbar machen
        pygame.mouse.set_visible(self.mouse_visible) #status der maus --> ob sichtbar oder nicht abhaengig von "self.mouse_visible" machen

        #import stuff
        self.data = Data() 


        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #Screen von settingsclass
        pygame.display.set_caption('Time_traveller') #namen des fensters aendern
        self.clock = pygame.time.Clock() #clock einfuehren
        
        


        

        #import menu
        self.esc_menu = EscMenu(self.screen)
        self.esc_pressed = False
        #states:
        self.level = Level(self.data)

    def draw_mouse(self):
        self.mouse_visible = True
        mouse_x , mouse_y = pygame.mouse.get_pos()
        
        pygame.draw.circle(surface = self.screen,
                color  =  (0, 0, 139),
                center = (mouse_x, mouse_y), 
                radius = SCREEN_HEIGHT // 120)


    def activate_esc_menu(self):
        self.esc_menu.check_4_esc_menu_active()

    def run(self):
        self.screen.fill((0,0,0)) # bildschirm mit schwarzer farbe fuellen
        while True:
            self.keys = pygame.key.get_pressed() # ueberpruefung zustands aller tasten --> gedrueckt oder nicht
            for event in pygame.event.get(): # ueberpruefung aller events
                if event.type == pygame.QUIT: # wenn das fenster geschlossen wird
                    pygame.quit() # beenden von pygame
                    sys.exit() # beenden des programms 

                if event.type == pygame.KEYDOWN: # wenn eine taste gedrueckt wird
                    if event.key == pygame.K_ESCAPE: # wenn die taste ESCAPE ist
                        self.esc_pressed = not self.esc_pressed # setze self.esc_pressed auf: nicht self.esc_pressed (macht gegenteil vom voherigen zustand) 
                        if self.esc_pressed: # wenn self.esc_pressed == True
                            self.activate_esc_menu() # esc_menu anzeigen

                if self.esc_menu.button_pressed_exit == True: # ueberpruefung ob exit-button im ESC-Menue gedrueckt
                    self.running = False
                    pygame.quit() # beenden von pygame
                    sys.exit() # beenden des programms                  
                
            dt = self.clock.tick(60) / 1000 # berechnung framerate
            
            self.level.run(dt) # laesst die methode run in level.py laufen

            if self.esc_pressed: # wenn esc gedrueckt
                self.esc_menu.run() # ausfuehren der methode --> zeigt die button an
                self.draw_mouse() # anzeigen der mouse
            pygame.display.update() # aktualisierung bildschirm mit neuen grafiken und inhalten

if __name__ == '__main__':
    game = Game()
    game.run()