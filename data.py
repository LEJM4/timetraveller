# enthaelt daten ueber das spieler inventar
# und ueber die direkten missionen
# kann dennoch mit z.b. setttings oder game_data zusammengefasst werden

class Data:
    def __init__(self):
        self.blueberry = 0
        self.raspberry= 0
        self.coin = 0

lvl = {1: False,
       2: False,
       3: False}

player_inventory = {
    'blueberry': 0,
    'coins': 0,
    'corps': 0,
    'raspberry': 0,
}



missions_text = {'lvl_1': ['Sammle 4 Beeren.' , 'Sprich mit dem Computer.', 'Töte 3 Gegner.'],
           'lvl_2': ['__', '__', '__']}



# print(lvl[1])
# print('')
# lvl[1] = False
# print(lvl[1])

# print('')
# print(lvl)
