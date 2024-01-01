from pathlib import Path
from classes_modules import Player, Land


def parse_level(filename: str):
    path = Path(__file__).parent.parent / 'assets' / 'levels' / f'{filename}.txt'

    player = None
    level_objects = []
    with open(path, encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip().split()
            type, data = line[0], [int(i) for i in line[1:]]
            if type == '.':
                player = Player(*data)
            elif type == '_':
                level_objects.append(Land(*data))

    if player is None:
        raise Exception('не нашел игрока на уровне')

    return player, level_objects