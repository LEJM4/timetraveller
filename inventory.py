from settings import *
from button import Button
from geometrie import *

# prototyp fuer ein inventar 

class Inventory:
    def __init__(self, screen):
        self.screen = screen
        
        self.first_x = button_pos['inventory'][0][0]
        self.first_y = button_pos['inventory'][0][1]
        #self.first_y = SCREEN_HEIGHT // 2
        self.box_height = SCREEN_WIDTH // 12
        self.box_width = self.box_height
        self.border_thickness = int(self.box_height // 20)  
        self.slots = [Rectangle(screen= self.screen,
                                  color = (50, 62, 79, 150),
                                  color_2= 'white',
                                  rect= (self.first_x + i*(self.box_height) - i*self.border_thickness , self.first_y, self.box_width, self.box_height ),
                                  border = True,
                                  border_color= 'white')
                                  for i in range (0,6) ]
        self.active_box = None # setzt active box auf none

    def update_inv(self, dt):
        keys = pygame.key.get_pressed()
        mouse_button_down = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()
        boxes = [(index, box) for index, box in enumerate(self.slots) if mouse_button_down and box.collidepoint(mouse_pos)]
        boxes_1 = [box for box in self.slots if mouse_button_down and box.collidepoint(mouse_pos)]
        # index = zahl zwischen 0 und 5 und steht fuer die box der reihenfolge aufsteigend
        # box in enumerate (boxen werden von 0 - 5 numeriert) 
        #nur wenn mouse button down und der collidepoint mit mouse_pos vorhanden ist
        if boxes_1:
            
            print(len(boxes))
            print(boxes_1)
            print(len(boxes_1))
            self.active_box = boxes[0][0]  # boxes [liste aller boxen][box_index]
            print(f"numemr {self.active_box}")
            #x,y, w, h = boxes[0].rect
            #print(x,y)
        else:
            self.active_box = None
            

    def display(self):

        for button in self.slots:
            button.draw()
        self.update_inv('a')


#"""

pygame.init()
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

inv = Inventory(display_surface)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit
        display_surface.fill((2,0,100))
        inv.display()
        pygame.display.update()
#"""

