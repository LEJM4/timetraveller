import pygame, sys
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from level import Level
from install_requirements import installieren_aller_requirements


installieren_aller_requirements()

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption('Time_traveller')
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):

        
        while True:
            #self.keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # if self.keys[pygame.K_ESCAPE]:
                #     pygame.quit()
                #     sys.exit()
                
            dt = self.clock.tick() / 1000
            self.level.run(dt)
            pygame.display.update()



if __name__ == '__main__':
    game = Game()
    game.run()