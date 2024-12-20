from settings import *
from support import *

# formen welche beispielsweise fuer ui gebraucht werden --> kreise werden gruen (wenn mission erledigt)

class Circle:
    def __init__(self, screen, color, color_2, center, radius):
        self.screen = screen #display surf
        self.color = color
        self.color_2 = color_2
        self.center = center #x und y
        self.radius = radius


    def draw(self):
        pygame.draw.circle(surface=self.screen, color=self.color, center=self.center, radius=self.radius)

    def change_color(self):
        self.color = self.color_2

class Rectangle:
    def __init__(self, screen, color, rect: tuple, color_2 = 'white', border_color = 'red', border = False):
        self.screen = screen
        self.color = color
        self.color_2 = color_2
        self.border_color = border_color
        self.rect = rect # (x-koordinate, y-koordinate, breite, hoehe)
        self.center = (self.rect[2] // 2 , self.rect[3] // 2)
        print(self.center)
        self.border = border
        self.border_thickness =  int(self.rect[3] // 20)  # Rahmendicke


    def draw(self):
        pygame.draw.rect(surface=self.screen, color=self.color, rect=self.rect)
        if self.border:
            self.draw_border()


    def change_color(self):
        self.color = self.color_2


    def draw_border(self):
        pygame.draw.rect(self.screen, self.border_color, self.rect, width=self.border_thickness)

    def collidepoint(self, pos):
        x, y, w, h = self.rect #--> nimmt die werte aus dem tuple und packt sie eben in die variablen
        return x <= pos[0] <= x + w and y <= pos[1] <= y + h
        # #prueft ob die x kordnt von pos[0] zwischen linker kante d. rects (x) und rechter kante d. rects (x + w) liegt #--> andere prueft die hoehe
        # gibt true oder false zurueck

