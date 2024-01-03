import sys
import os
import pygame
import pygame_gui

size = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(size)
screen.fill('white')


def load_image(name, colorkey=None):
    fullname = os.path.join('../assets', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Land(pygame.sprite.Sprite):
    def __init__(self, image, x1, y1, dlinna, vysota):
        super().__init__(all_sprites)
        self.rect = pygame.Rect(x1, y1, dlinna, vysota)
        self.image = pygame.transform.scale(load_image(f'fons/{image}'), self.rect.size)
        self.mask = pygame.mask.from_surface(self.image)


class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = pygame.transform.scale(load_image(f'objects/{image}'), (64, 64))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(pos_x, pos_y)


class Wall(pygame.sprite.Sprite):
    def __init__(self, image, x1, y1, dlinna, vysota):
        super().__init__(all_sprites)
        self.rect = pygame.Rect(x1, y1, dlinna, vysota)
        self.image = pygame.transform.scale(load_image(f'fons/{image}'), self.rect.size)
        self.mask = pygame.mask.from_surface(self.image)

# class Lever(pygame.sprite.Sprite):
#     def __init__(self, image, x1, x2):
#         pass



horizontal_borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player_image = pygame.transform.scale(load_image('objects/lico.jpg'), (64, 64))
