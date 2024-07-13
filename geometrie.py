from settings import *
from support import *



class Circle:
    def __init__(self, screen, color, color_2, center, radius):
        self.screen = screen
        self.color = color
        self.color_2 = color_2
        self.center = center
        self.radius = radius

    def draw(self):
        pygame.draw.circle(surface=self.screen, color=self.color, center=self.center, radius=self.radius)

    def change_color(self):
        self.color = self.color_2


class Rectangle:
    def __init__(self, screen, color, color_2, rect: tuple):
        self.screen = screen
        self.color = color
        self.color_2 = color_2
        self.rect = rect

    def draw(self):
        pygame.draw.rect(surface=self.screen, color=self.color, rect=self.rect)

    def change_color(self):
        self.color = self.color_2