import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from button import Button
import sys
import time
from settings import *


class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        button_width = SCREEN_WIDTH // 4
        button_height = SCREEN_HEIGHT // 6
        button_space = SCREEN_HEIGHT // 20  # abstand zwischen buttons

        # position buttons berechnen
        start_x = SCREEN_WIDTH // 2 - button_width // 2
        start_y = SCREEN_HEIGHT // 2 - (button_height + button_space)
        exit_y = start_y + button_height + button_space

        # buttons erstellen
        self.start_button = Button("Start", start_x, start_y, button_width, button_height, screen)
        self.exit_button = Button("Exit", start_x, exit_y, button_width, button_height, screen)
        
        pygame.mouse.set_visible(False)

    def draw_mouse(self):
        self.mouse_visible = True
        mouse_x , mouse_y = pygame.mouse.get_pos()
        
        pygame.draw.circle(surface = self.screen,
                color  =  (0, 0, 139),
                center = (mouse_x, mouse_y), 
                radius = SCREEN_HEIGHT // 120)
        
    def run(self):
        while self.running:
            self.screen.fill("cyan")  # hintergrundfarbe
            self.start_button.draw(self.screen)
            self.exit_button.draw(self.screen)
            self.draw_mouse()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # linksklick
                    mouse_pos = pygame.mouse.get_pos()
                    if self.start_button.is_clicked(mouse_pos):
                        self.running = False  # startscreen schliessen
                    if self.exit_button.is_clicked(mouse_pos):
                        self.exit_game()

            pygame.display.flip()

    def exit_game(self):
        pygame.quit()
        sys.exit()

"""
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("startbildschirm")
        self.start_screen = StartScreen(self.screen)

    def run(self):
        self.start_screen.run()
        self.game_loop()

    def game_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((0, 128, 255))
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
#"""