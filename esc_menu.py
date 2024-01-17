import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

class Button:
    def __init__(self, text, x_position, y_position):
        self.text = text
        self.x_position = x_position
        self.y_position = y_position
        

    def draw_buttons (self):
        button_rect = pygame.rect.Rect((self.x_position, self.y_position) , (SCREEN_WIDTH/10 , SCREEN_HEIGHT/25))



class Esc_Menu:
    def __init__(self):
        pass