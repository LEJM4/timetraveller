from button import Button
from settings import *
from support import *
from sys import exit
from geometrie import *
from data import *
class UserInterface:
    def __init__(self, screen, current_lvl: str):
        self.screen = screen
        self.current_lvl = current_lvl
        self.circle_color = (20,145 , 242)
        self.circle_color_2 = (30, 102, 79, 200)


        self.check_mark = import_image('graphics', 'ui', 'check_mark_green')
        self.mission_buttons = [  #creates a list with all buttons


            #background rect 
            Button(text= '',
                   x_position=int(button_pos['missions'][0][0]) -10,  #start pos = (10,10)
                   y_position=int(button_pos['missions'][0][1]) -10, 
                   button_width=int(button_size['missions'][0]) + 20, #button erst 10 nach links -> um wiedeer die 10 rechts abzudecken insgesamt 20 --> 
                   button_height= 3* (button_size['missions'][1]) + 3 *int(button_size['missions'][0] / 40) + 10, #3 * hoehe button + 3* border (siehe class button) + 10 --> abstand zwischen den einzelnen butten --> settings class
                   screen=screen,
                   border = True,
                   collision_allowed=False,
                   button_color = (50, 62, 79, 200)),


            #mission 1 
            Button(text=missions_text[self.current_lvl][0], #get text from settings
                   x_position=int(button_pos['missions'][0][0]), #from settings dict
                   y_position=int(button_pos['missions'][0][1]), #from settings dict
                   button_width=int(button_size['missions'][0]), #from settings dict
                   button_height=button_size['missions'][1],#from settings dict
                   screen=screen, 
                   border = True,
                   collision_allowed=False,
                   #button_color= 'grey',
                   font_size=0.65),


            #mission 2
            Button(text=missions_text[self.current_lvl][1],
                   x_position=int(button_pos['missions'][1][0]), 
                   y_position=int(button_pos['missions'][1][1]), 
                   button_width=int(button_size['missions'][0]), 
                   button_height=button_size['missions'][1],
                   screen=screen,
                   border = True,
                   collision_allowed=False,
                   font_size=0.65),

            #mission 3
            Button(text=missions_text[self.current_lvl][2],
                   x_position=int(button_pos['missions'][2][0]), 
                   y_position=int(button_pos['missions'][2][1]), 
                   button_width=int(button_size['missions'][0]), 
                   button_height=button_size['missions'][1],
                   screen=screen,
                   border = True,
                   collision_allowed=False,
                   font_size=0.65) 
        ]

        self.circles = [
            Circle(screen=screen,
                   color=self.circle_color,
                   color_2=self.circle_color_2,
                   center=(SCREEN_WIDTH // 4.02, int(button_pos['missions'][0][1]) + (button_size['missions'][1] // 2)),
                   radius=button_size['missions'][1] // 4),
            Circle(screen=screen,
                   color=self.circle_color,
                   color_2=self.circle_color_2,
                   center=(SCREEN_WIDTH // 4.02, int(button_pos['missions'][1][1]) + (button_size['missions'][1] // 2)),
                   radius=button_size['missions'][1] // 4),
            Circle(screen=screen,
                   color=self.circle_color,
                   color_2=self.circle_color_2,
                   center=(SCREEN_WIDTH // 4.02, int(button_pos['missions'][2][1]) + (button_size['missions'][1] // 2)),
                   radius=button_size['missions'][1] // 4)
        ]


    def display(self):

        for button in self.mission_buttons:
            button.draw(self.screen)
        
        for circle in self.circles:
            circle.draw()

        if lvl[1]: self.circles[0].change_color() 
        if lvl[2]: self.circles[1].change_color() 
        if lvl[3]: self.circles[2].change_color() 
	    

"""

pygame.init()
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ui = UserInterface(display_surface, 'lvl_1')


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit
        display_surface.fill((2,0,100))
        ui.display()
        pygame.display.update()
#"""