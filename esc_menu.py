import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from main import *
class Button:
    def __init__(self, text, x_position, y_position, button_width , button_height):
        self.text = text
        self.x_position = x_position
        self.y_position = y_position
        self.button_width = button_width
        self.button_height = button_height
        

    def draw_buttons (self):
        button_rect = pygame.rect.Rect((self.x_position, self.y_position) , (SCREEN_WIDTH/10 , SCREEN_HEIGHT/25), 100, 50)
        pygame.draw.rect()


class Esc_Menu:
    def __init__(self):
        pass