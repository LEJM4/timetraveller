import pygame
from os import walk
from settings import *
from os.path import join
from os import walk
from pytmx.util_pygame import load_pygame
from sys import exit
from pygame.math import Vector2 as vector 

# enthaelt die funktionen, die fuer das importieren von daten wichtig sind

#_________________________________________________________________________________________________________________________
#NICHT MEHR VERAENDERN BIS!!!!

#tilemap
def tmx_importer(*path):
    tmx_dict = {} 
    # neues dictionary --> speichert spaeter tmx-dateien

    for folder_path, sub_folders, file_names in walk(join(*path)):
        # durchlaeuft alle ordner, unterordner und dateien im angegebenen pfad.
        # 'folder_path' --> aktueller ordnerpfad
        # 'sub_folders' --> liste unterordner im aktuellen ordner
        # 'file_names' --> liste dateinamen im aktuellen ordner

        for file in file_names:
            # iteration durch alle dateien im aktuellen ordner

            tmx_dict[file.split('.')[0]] = load_pygame(join(folder_path, file))
            # key = name der datei ohne die dateiendung (file.split('.')[0])
            # datei wird mit funktion `load_pygame` geladen und im dict gespeichert

    return tmx_dict
    # gibt tmx_dict mit allen tmx-dateien zurueck



# image and map stuff
def import_image(*path, alpha = True, format = 'png', scale = SCALE_FACTOR): 
    # (pfad zur datei, alpha kanal, format, vergroesserungsfaktor)

	full_path = join(*path) + f'.{format}' 
    # join --> geht den dateipfad vom aktuellen verzeichnis zur datei + ".format"

	surf = pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
    # falls alpha True --> convert.alpha(), wenn nicht dann nur convert()

	return pygame.transform.scale_by(surf, scale)
    # gibt das bild transformiert (vergroessert oder verkleinert) um den faktor "scale" zurueck



def import_animation_frames(cols, rows, *path, scale = SCALE_FACTOR):
    frames = []
    # liste enthaelt spaeter die einzelnen frames fuer die animation 

    surf = import_image(*path, scale = scale)
    # laden des bilds mit funktion `import_image` und evt. skalieren

    cell_width, cell_height = surf.get_width() / cols, surf.get_height() / rows
    # definiert die breite einer zeile und spalte
    # zellenbreite = breite von surf / anzahl der spalten
    # zellenhoehe = hoehe von surf / anzahl der zeilen

    for row in range(rows):
        for col in range(cols):
            cutout_rect = pygame.Rect(col * cell_width, row * cell_height, cell_width, cell_height)
            # definiert einen rechteck bereich (cutout_rect) 
            # --> dieser repraesentiert aktuelles tile in tilemap


            cutout_surf = pygame.Surface((cell_width, cell_height), pygame.SRCALPHA)
            # erstellt neue oberflaeche (surface) fuer einzelnes tile (cell_width, cell_height)
            # "pygame.SRCALPHA" --> sorgt dafuer, dass oben erstellte oberflaeche 
            # --> alpha-kanal (transparenz) unterstuetzt

            cutout_surf.blit(surf, (0, 0), cutout_rect)
            # zeichnet das aktuelle tile aus der tilemap auf die neue oberflaeche 
            # --> also auf cutout_rect

            frames.append(cutout_surf)
            # fuegt ausgeschnittenes frame der liste frames hinzu
    
    return frames
    # gibt frames zurueck --> enthaelt animation in aufsteigender reihenfolge



def import_spritesheet(cols, rows, *path, scale = SCALE_FACTOR):
    # spritesheet mit (spalten, reihen(zeilen), pfad zur datei) 

	frames = {} # erstellt ein leeres Dictionary, welches spaeter gefuellt wird
	surf = import_image(*path, scale = scale) # laedt mithilfe der funktion "import_image" die tilemap
      
	cell_width, cell_height = surf.get_width() / cols, surf.get_height() / rows
    # definieren von zeile und spalte
    # zellenbreite = breite von surf / anzahl der spalten
    # zellenhoehe = hoehe von surf / anzahl der zeilen

	for col in range(cols):
		for row in range(rows):
			cutout_rect = pygame.Rect(col * cell_width, row * cell_height,cell_width,cell_height)
            # definiert einen rechteck. bereich (cutout_rect) 
            # --> dieser repraesentiert das aktuelle tile im spritesheet
            
			cutout_surf = pygame.Surface((cell_width, cell_height))
            # erstellt oberflaeche fuer das einzelne tile

			cutout_surf.fill('green')
            # fuellt cutout_surf mit gruen aus --> nur als platzhalter fuer das spaetere bild

			cutout_surf.set_colorkey('green')
            # setzt gruen als transparente farbe (colorkey) --> damit gruene fuellung unsichtbar wird 

			cutout_surf.blit(surf, (0,0), cutout_rect)
            # zeichnet aktuelle tiles aus tilemap auf die neue oberflaeche 
            # --> also auf cutout_rect

			frames[(col, row)] = cutout_surf
            # speichert tile im dictionary 'frames' unter dem key (schluessel) (col, row)

	return frames
    # gibt das dictionary zurueck --> (enthaelt alle tiles aus dem spritesheet)



def spritesheet_vertical(cols, row, *path, scale = SCALE_FACTOR):
	frame_dict = import_spritesheet(cols, row, *path, scale = scale)
    # laedt das spritesheet und speichert es als ein dictionary: frame_dict
    # schluessel sind (col, row) und werte sind entsprechenden frames
    
	new_dict ={}
    # erstellt ein neues dictionary --> um spater die frames nach bewegungsrichtung zu speichern

	for row, direction in enumerate(('down','left', 'right','up')):
        # iteriert durch jede zeile des spritesheets --> ordnet frames den richtungen zu
        # reihenfolge: "down", "left", "right", "up"

		new_dict[direction] = [frame_dict[(col, row)] for col in range(int(cols))]
        # jeder richtung wird eine liste von frames zugeordnet --> die in der jeweiligen zeile liegen
        # "col" ist dabei die aktuelle spalte
        
	return new_dict
    # gibt new_dict zurueck --> enthaelt frames sortiert nach bewegungsrichtungen 



def import_character_animation(cols, rows, *path, scale = SCALE_FACTOR):
    frame_dict = import_spritesheet(cols, rows, *path, scale = scale)
    # laden des spritesheets --> speichern in dictionary aus der funktion 'import_spritesheet'
     
    new_dict = {
        'idle': {'down': [], 'up': [], 'left': [], 'right': []},
        'move': {'down': [], 'up': [], 'left': [], 'right': []},
        'attack': {'down': [], 'up': [], 'left': [], 'right': []},
        'collect': {'down': [], 'up': [], 'left': [], 'right': []},
        'dead': [], 
        'hold_item': [], 
        'special_1': [], 
        'special_2': []
    }
    # dieses dictionary enthaelt alle moeglichen animationen, welche der charakter ausfuehren kann 

    # row 1 --> idle animation
    for col, direction in enumerate(('down', 'up', 'left', 'right')):
        # jede richtung erhaelt das entsprechende frame aus der ersten feihe
        new_dict['idle'][direction] = [frame_dict[(col, 0)]]

    # row 0 - 4 --> move animation
    for row in range(0, 4):
        for col, direction in enumerate(('down', 'up', 'left', 'right')):
        # jede richtung erhaelt das entsprechende frame aus der reihe 1 bis 4
            new_dict['move'][direction].append(frame_dict[(col, row)])

    # row 5 --> attack animation
    for col, direction in enumerate(('down', 'up', 'left', 'right')):
        # jede richtung erhaelt das entsprechende frame aus der reihe 5
        new_dict['attack'][direction] = [frame_dict[(col, 4)]]

    # row 6 --> collect animation
    for col, direction in enumerate(('down', 'up', 'left', 'right')):
        # jede richtung erhaelt das entsprechende frame aus reihe 6
        new_dict['collect'][direction] = [frame_dict[(col, 5)]]

    # row 7--> seperate animation:  dead, hold_item, special_1, special_2
    for col, key in enumerate(('dead', 'hold_item', 'special_1', 'special_2')):
        # siebte reihe (row 6) wird fuer die separaten animationen:
        # 'dead', 'hold_item', 'special_1' , 'special_2' verwendet
        new_dict[key] = [frame_dict[(col, 6)]]
    
    return new_dict
    # gibt dictionary 'new_dict' zurueck --> mit allen moeglichen animationen des charakters

# BIS HIERHIN!!!
#_________________________________________________________________________________________________________________________

def spritesheet_horizontal(cols, rows, *path):
	frame_dict = import_spritesheet(cols, rows, *path)
	new_dict = {}
	for col, direction in enumerate(('down','up', 'left','right')):
		new_dict[direction] = [frame_dict[(col, row)] for row in range(rows)]
	return new_dict

def spritesheet_vertical_projectile(cols, row, *path):
	frame_dict = import_spritesheet(cols, row,*path)
	new_dict ={}
	for row, direction in enumerate(('up','left', 'right','down')):
		new_dict[direction] = [frame_dict[(col, row)] for col in range(int(cols))]
		#new_dict[f'{direction}_idle'] = [frame_dict[(0, row)]]
	return new_dict



def import_all_characters(cols, rows, *path):
    character_assets = {}
    # leeres dictionary

    for folder_path, sub_folders, _ in walk(join(*path)):
        # geht durch alle unterordner im angegebenen pfad --> 'folder_path' = aktueller ordnerpfad
        # 'sub_folders' = liste der unterordner
        # '_' steht fuer dateinamen --> da diese keine rolle spielen bzw. nicht verwendet werden
        # --> verwendet man '_'

        for sub_folder in sub_folders:
            character_name = sub_folder
            character_path = join(folder_path, sub_folder)
            # nutzt den charakter-namen als namen des unterordners 
            # --> erstellt vollstaendigen pfad zum charakter-ordner

            sprite_sheet_path = join(character_path, "SpriteSheet")
            # sucht nach datei "SpriteSheet.png" bzw. "Faceset" in jedem unterordner
            faceset_path = join(character_path, "Faceset")
            # pfade zu "SpriteSheet.png" bzw. "Faceset" werden definiert



            
            character_assets[character_name] = {
                'animation': import_character_animation(cols, rows, sprite_sheet_path),
                # anwendung funktion: import_character_animation 

                'faceset': import_image(faceset_path)
                # laden von "faceset.png" mit der funktion: import_image
            }
            # character_animation --> uebergeben von cols, rows und pfad zum SpriteSheet
            # schluessel = animation im dictionary fuer den charakter
            # laden des faceset mit: import_image --> schluessel = faceset
    
    return character_assets
    # gibt dictionary mit allen animationen und facesets von den charakteren zurueck


#map 
def check_distance(radius, target, entity):
	distance_vector = (vector(target.rect.center) - vector(entity.rect.center)) 
	#distance_vector = vector vom spieler - vector vom zombie
	distance_squared = distance_vector.length_squared()
	radius_squared = radius**2
	return distance_squared < radius_squared



