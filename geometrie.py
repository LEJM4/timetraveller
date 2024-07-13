from settings import *
from support import *



class Circle:
    def __init__(self, screen, color, color_2, center, radius):
        self.screen = screen #display surf
        self.color = color
        self.color_2 = color_2
        self.center = center #x und y
        self.radius = radius
        self.check_mark = import_image('graphics', 'ui', 'check_mark_green')
        self.scaled_check_mark = pygame.transform.scale(self.check_mark, (self.radius * 2, self.radius * 2))
        #                                               (was = check_mark, (2*radius = durchmesser , 2*radius = durchmesser )


    def draw(self):
        pygame.draw.circle(surface=self.screen, color=self.color, center=self.center, radius=self.radius)

    def change_color(self):
        self.color = self.color_2

    def draw_check_mark(self):
        self.screen.blit(self.scaled_check_mark, (self.center[0] - self.scaled_check_mark.get_width() // 2, self.center[1] - self.scaled_check_mark.get_height() // 2))
    #                    (was = scaled_check_mark,  (x-koordinate) - haelfte der breite (des bildes)      ,   (y-koordinate)-  haelfte der hoehe des bildes )


class Rectangle:
    def __init__(self, screen, color, color_2, rect: tuple):
        self.screen = screen
        self.color = color
        self.color_2 = color_2
        self.rect = rect # (x-koordinate, y-koordinate, breite, hoehe)

    def draw(self):
        pygame.draw.rect(surface=self.screen, color=self.color, rect=self.rect)

    def change_color(self):
        self.color = self.color_2