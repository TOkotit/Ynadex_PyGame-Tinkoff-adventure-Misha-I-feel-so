from pathlib import Path
from classes_modules import *


def parse_level(filename: str):
    path = Path(__file__).parent.parent / 'assets' / 'levels' / f'{filename}.txt'

    player = None
    level_objects = []
    player_objeccts = []
    with open(path, encoding='utf-8') as f:
        for line in f.readlines():
            if line[0] == '#':
                level_fon = ' '.join(line.strip().split()[1:])
            elif line[0] == 'M':
                bg_music = ' '.join(line.strip().split()[1:])

            else:
                line = line.strip().split()
                type, data, image = line[0], [int(i) for i in line[1:-1]], line[-1]
                if type == '.':
                    player = Player(image, *data)
                elif type == '_':
                    level_objects.append(Land(image, *data))
                elif type == '|':
                    level_objects.append(Wall(image, *data))
                elif type == '/':
                    player_objeccts.append(Lever(image, *data))

    if player is None:
        raise Exception('не нашел игрока на уровне')

    return player, level_fon, level_objects, player_objeccts, bg_music