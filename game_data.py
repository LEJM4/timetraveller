# verwaltung der ingame daten
from settings import hit_points

LIFE_DATA = {
	'player': {
		'health': hit_points['player'],
		'defeated': False,
		},
    'o1': {
		'health': hit_points['zombie_1'],
		'defeated': False,
		},
	'o2': {
		'health': hit_points['zombie_2'],
		'defeated': False,
		},
	'o3': {
		'health': hit_points['zombie_1'],
		'defeated': False,
		},
	'o4': {
		'health': hit_points['zombie_1'],
		'defeated': False,
		},
	'o5': {
		'health': hit_points['zombie_1'],
		'defeated': False,
		},
	'o6': {
		'health': hit_points['zombie_1'],
		'defeated': False,
		},
	'o7': {
		'health': hit_points['zombie_1'],
		'defeated': False,
		},
	'o8': {
		'health': hit_points['zombie_1'],
		'defeated': False,
		},
	'o9': {
		'health': hit_points['zombie_1'],
		'defeated': False,
		},
}

Character_DATA = {
	'robo': {
		'health': 6,
		'dialog': {
			'1': ['Nah, wie geht es dir?', 'In der Stadt sind viele Monster\n die Unheil angerichtet haben!', 'Töte diese Kreaturen!'], 
			'2': ['Hallo', 'was geht']},
		'current_dialog': 1,
        'can_talk': True
		}
}