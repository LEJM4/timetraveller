from install_requirements import installieren_aller_requirements


#installieren_aller_requirements()

import pygame, sys
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from level import Level
from data import Data   
from esc_menu import EscMenu



class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption('Time_traveller')
        self.clock = pygame.time.Clock()

        #import stuff
        self.data = Data()

        #import menu
        self.esc_menu = EscMenu(self.screen)
        self.esc_pressed = False
        #states:
        self.level = Level(self.data)


    def activate_esc_menu(self):
        self.esc_menu.check_4_esc_menu_active()

    def run(self):
        self.screen.fill((0,0,0))

        
        while True:
            self.keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if self.keys[pygame.K_BACKSPACE]:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.esc_pressed = not self.esc_pressed #macht immer das gegenteil von dem Zustand 
                        self.activate_esc_menu()
                        


                if self.esc_menu.button_pressed_exit == True:
                    self.running = False
                    pygame.quit()
                    sys.exit()                   

                    
                
            dt = self.clock.tick() / 1000
            
            self.level.run(dt)

            if self.esc_pressed:
                self.esc_menu.run()

            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()