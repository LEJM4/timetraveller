import pygame
from settings import font_path

class Button:
    def __init__(self, text, x_position, y_position, button_width, button_height, screen):
        
        #screen
        self.screen = screen
        #button rect
        self.x_position = x_position  #x pos von button
        self.y_position = y_position   #y pos von button
        self.button_width = button_width #breite von button
        self.button_height = button_height #hoehe von button

        self.button_color = pygame.Color(50, 62, 79, 150)  # rgba  a=200 für weniger transparenz

        self.button_rect = pygame.Rect(self.x_position, self.y_position, self.button_width, self.button_height)  


        #button text        
        self.text = text
        self.font_size = int(0.78* self.button_height) #font
        self.text_color_normal = (255, 255 ,255)  # weiss
        self.font = pygame.font.Font(font_path, self.font_size)

        self.text_surf = self.font.render(self.text, True, self.text_color_normal)  #(zu rendernder text , glattere Kanten, textfarbe) 
        self.text_rect = self.text_surf.get_rect(center=self.button_rect.center)  #text pos  
        
        self.text_color_overlap = (0,255,0) #ovberlap

        #mouse
        self.mouse_pressed = False
        self.button_is_pressed = False

    def button_border(self):
        border_color = self.text_color_overlap  # 
        border_thickness = int(self.button_width / 80) # dicke rahmen
        
        # Rahmen 
        pygame.draw.rect(self.screen, border_color, self.button_rect, border_thickness)

    def draw(self, screen):
        # create button rect

        # Transparente oberfläche für button 
        button_surface = pygame.Surface((self.button_width, self.button_height), pygame.SRCALPHA)
        button_surface.fill(self.button_color)   #oberfläche mit transp. Farbe

        # Button-Oberfläche und Text zeichnen
        screen.blit(button_surface, (self.x_position, self.y_position))
        screen.blit(self.text_surf, self.text_rect)

        self.button_collision()

    def button_collision(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_get_pressed_left = pygame.mouse.get_pressed()[0] #[0] = linke Maustaste ;[1] = Mausrad ; [2] = rechte Maustaste

        if self.button_rect.collidepoint(mouse_pos):
            self.text_surf = self.font.render(self.text, True, self.text_color_overlap)
            
            self.button_border()

            if mouse_get_pressed_left:

                self.mouse_pressed = True
                self.button_is_pressed = True
                print(self.button_is_pressed)

            else:
                if self.mouse_pressed == True:
                    print('click')
                    self.mouse_pressed = False
        else:
            self.text_surf = self.font.render(self.text, True, self.text_color_normal)

    def button_clicked(self):
        if self.button_is_pressed:
            self.button_is_pressed = False  # Button zustand zurücksetzen
            return True
        return False
