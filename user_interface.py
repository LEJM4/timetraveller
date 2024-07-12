from button import Button
from settings import *

from sys import exit

class UserInterface:
    def __init__(self, screen, current_lvl: str):
        self.screen = screen
        self.current_lvl = current_lvl
        self.circle_color = (30, 102, 79, 200)

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


    def display(self):

        for button in self.mission_buttons:
            button.draw(self.screen)
	    

        
        #top circle
        pygame.draw.circle(surface=self.screen,
                            color= self.circle_color,
                            center= (SCREEN_WIDTH //4.02, (int(button_pos['missions'][0][1]) + (button_size['missions'][1] // 2))), #x = zufaellig gefunden --> y button pos 6 haelfte der hoehe des buttons
                            radius=button_size['missions'][1] //4)

        #middle circle
        pygame.draw.circle(surface=self.screen,
                            color= self.circle_color,
                            center= (SCREEN_WIDTH //4.02, (int(button_pos['missions'][1][1]) + (button_size['missions'][1] // 2))), #x = zufaellig gefunden --> y button pos 6 haelfte der hoehe des buttons
                            radius=button_size['missions'][1] //4)

        #bottom circle
        pygame.draw.circle(surface=self.screen,
                            color= self.circle_color,
                            center= (SCREEN_WIDTH //4.02, (int(button_pos['missions'][2][1]) + (button_size['missions'][1] // 2))), #x = zufaellig gefunden --> y button pos 6 haelfte der hoehe des buttons
                            radius=button_size['missions'][1] //4)

#'''
pygame.init()
ds = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#aa = (character_image_importer(4, 7, 'graphics','character', 'move'))
ui = UserInterface(ds, 'lvl_1')
#b = Button(text,0,0,SCREEN_WIDTH//3, SCREEN_HEIGHT//3, ds)
#aa = (import_spritesheets('graphics','player'))

#print(aa)

#print(aa['move']['left'])

#print(len(aa['move']['left']))


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
	ds.fill((0,88,0))
	#pygame.draw.rect(ds, 'blue',(10,10, SCREEN_WIDTH //3.5, SCREEN_HEIGHT//3),200, 20)
	ui.display()
    #pygame.draw.rect(ds, 'blue',(0,0,0,0),200, 20)
	pygame.display.update()

#'''