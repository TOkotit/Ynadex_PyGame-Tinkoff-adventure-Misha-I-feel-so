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


class Lever(pygame.sprite.Sprite):
    def __init__(self, image, x1, y1, dlinna, vysota, *condotions):
        super().__init__(all_sprites)
        self.sound = pygame.mixer.Sound('../assets/sounds/lever_sound.mp3')
        self.sound.set_volume(0.3)
        self.conditions = condotions
        self.rect = pygame.Rect(x1, y1, dlinna, vysota)
        self.image = pygame.transform.scale(load_image(f'objects/{image}'), self.rect.size)
        self.mask = pygame.mask.from_surface(self.image)

    def touch(self):
        self.sound.play()
        self.image = pygame.transform.flip(self.image, True, False)

    def switch(self, exit__):
        for i in self.conditions:
            exit__.conditions[i - 1] = not exit__.conditions[i - 1]


class Exit(pygame.sprite.Sprite):
    def __init__(self, image, x1, y1, dlinna, vysota, coond):
        super().__init__(all_sprites)
        self.conditions = [False for i in range(coond)]
        self.exit_ = False
        self.rect = pygame.Rect(x1, y1, dlinna, vysota)
        self.image = pygame.transform.scale(load_image(f'objects/{image}'), self.rect.size)
        self.mask = pygame.mask.from_surface(self.image)

    def all_conditions_compled(self):
        if all(self.conditions):
            self.exit_ = True


class Indicator:
    def __init__(self, surface, ex):
        self.coonds = ex.conditions
        self.screen = surface
        self.color = {True: 'green', False: 'red'}
    def draw_circles(self):
        x = 42
        for i in range(len(self.coonds)):
            pygame.draw.circle(self.screen, pygame.Color(self.color[self.coonds[i]]), (x * (i + 1), 30), 20)

horizontal_borders = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player_image = pygame.transform.scale(load_image('objects/lico.jpg'), (64, 64))