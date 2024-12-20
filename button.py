import pygame
from settings import font_path

class Button:
    def __init__(self, text, x_position, y_position, button_width, button_height, screen, border = False, collision_allowed = True, button_color = (50, 62, 79, 150), font_size = 0.78, text_color = (255, 255 ,255)):
        # erschafft einen button 
        # verwendung in start- und esc-menu

        self.collision_allowed = collision_allowed
        self.border = border

        #screen
        self.screen = screen
        #button rect
        self.x_position = x_position  #x pos von button
        self.y_position = y_position   #y pos von button
        self.button_width = button_width #breite von button
        self.button_height = button_height #hoehe von button

        self.button_color = pygame.Color(button_color)  # rgba  a=200 für weniger transparenz

        self.button_rect = pygame.Rect(self.x_position, self.y_position, self.button_width, self.button_height)  


        #button text        
        self.text = text
        self.font_size = int(font_size* self.button_height) #font
        self.text_color_normal = text_color  # weiss
        self.font = pygame.font.Font(font_path, self.font_size)

        self.text_surf = self.font.render(self.text, True, self.text_color_normal)  #(zu rendernder text , glattere Kanten, textfarbe) 
        self.text_rect = self.text_surf.get_rect(center=self.button_rect.center)  #text pos  
        
        self.text_color_overlap =  (19, 15, 48, 0)#(0,255,0) #ovberlap

        #mouse
        self.mouse_pressed = False
        self.button_is_pressed = False

    def draw(self, screen):
    # zeichnet den button auf den screen

        # transparente oberflaeche fuer button 
        button_surface = pygame.Surface((self.button_width, self.button_height), pygame.SRCALPHA)
        button_surface.fill(self.button_color)   #oberflaeche mit transp. Farbe
        if self.collision_allowed:
            self.button_collision()
        
        # Button  und Text malen
        screen.blit(button_surface, (self.x_position, self.y_position))
        screen.blit(self.text_surf, self.text_rect)
        if self.border:
            self.button_border_and_size()
        


    def button_collision(self):
        # ueberprueft die button_collision
        mouse_pos = pygame.mouse.get_pos()
        mouse_get_pressed_left = pygame.mouse.get_pressed()[0] #[0] = linke Maustaste ;[1] = Mausrad ; [2] = rechte Maustaste

        if self.button_rect.collidepoint(mouse_pos): 
            self.button_border_and_size()

            if mouse_get_pressed_left:
                self.mouse_pressed = True
                self.button_is_pressed = True




            else:              
                if self.mouse_pressed == True:
                    #print('click')
                    self.mouse_pressed = False

                if self.button_is_pressed == True:
                    self.button_is_pressed = False
                    
        else:
            self.text_surf = self.font.render(self.text, True, self.text_color_normal)


    def button_border_and_size(self):
        # wenn die maus ueber den button geht, dann soll das visuell erkennbar sein
        border_color = self.text_color_overlap  
        border_thickness = int(self.button_width / 40) # dicke rahmen

        #change font color
        self.text_surf = self.font.render(self.text, True, self.text_color_overlap)
        
        # frame / Rahmen
        pygame.draw.rect(self.screen, border_color, self.button_rect, border_thickness)

    
    def is_clicked(self, mouse_pos):
        return self.button_rect.collidepoint(mouse_pos)