from pathlib import Path  # велика компания
from classes_modules import *  # загружаем все наши классы

# тут вобщем загружаются уровни

portals = {}  # список порталов


def parse_level(filename: str):  # выгружаем txt файл
    path = Path.cwd().parent / 'assets' / 'levels' / f'{filename}.txt'

    player = None
    level_objects = []
    player_objeccts = []
    with open(path, encoding='utf-8') as f:  # открываем
        for line in f.readlines():
            # в зависимости от ключа определяем объект
            match line[0]:
                case '#':
                    level_fon = ' '.join(line.strip().split()[1:])
                case 'S':
                    level_sky = ' '.join(line.strip().split()[1:])
                case 'M':
                    bg_music = ' '.join(line.strip().split()[1:])
                case 'P':
                    line = line.strip().split()
                    x, y, direction, id1, id2, image = int(line[1]), int(line[2]), line[3], int(line[4]), int(line[5]), \
                    line[-1]
                    portals[id1] = id2
                    level_objects.append(Portal(image, direction, id1, id2, x, y))

                case _:
                    line = line.strip().split()  # для разных классов свои параметры
                    type, data, image = line[0], [int(i) for i in line[1:-1]], line[-1]
                    match type:
                        case '.':
                            player = Player(image, *data)
                        case '_':
                            level_objects.append(Land(image, *data))
                        case '|':
                            level_objects.append(Wall(image, *data))
                        case '/':
                            player_objeccts.append(Lever(image, *data))
                        case 'E':
                            ex = Exit(image, *data)

    if player is None:  # ну он должен быть
        raise Exception('не нашел игрока на уровне')

    return player, level_fon, level_sky, level_objects, player_objeccts, bg_music, ex  # возвращаем что там в файле было написано
