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
        self.image = pygame.transform.smoothscale(load_image(f'fons/{image}'), self.rect.size)
        self.mask = pygame.mask.from_surface(self.image)


class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.idle_image = pygame.transform.smoothscale(load_image(f'objects/{image}'), (64, 64))
        self.image = self.idle_image
        self.orientation = 1
        self.cur_frame = 0
        self.run_frames = []
        self.fall_frames = []
        self.status = 'idle'
        self.cut_sheet(load_image(f'objects/tinkoff_run.png'), 20, 1, self.run_frames)
        self.cut_sheet(load_image(f'objects/tinkoff_fall_from_stratosphere.png'), 10, 1,self.fall_frames)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(pos_x, pos_y)
    def cut_sheet(self, sheet, colums, rows, list_):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // colums,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(colums):
                frame_location = (self.rect.w * i, self.rect.h * j)
                list_.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update_run(self):
        if self.status != 'run':
            self.status = 'run'
            self.cur_frame = 0
        self.image = self.run_frames[self.cur_frame]
        if self.orientation < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        self.cur_frame = (self.cur_frame + 1) % len(self.run_frames)
    def update_fall(self):
        if self.status != 'fall':
            self.status = 'fall'
            self.cur_frame = 0
        self.image = self.fall_frames[self.cur_frame]
        if self.orientation < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        self.cur_frame = (self.cur_frame + 1) % len(self.fall_frames)
    def update_idle(self):
        self.image = self.idle_image
        if self.orientation < 0:
            self.image = pygame.transform.flip(self.image, True, False)


class Wall(pygame.sprite.Sprite):
    def __init__(self, image, x1, y1, dlinna, vysota):
        super().__init__(all_sprites)
        self.rect = pygame.Rect(x1, y1, dlinna, vysota)
        self.image = pygame.transform.smoothscale(load_image(f'fons/{image}'), self.rect.size)
        self.mask = pygame.mask.from_surface(self.image)


class Lever(pygame.sprite.Sprite):
    def __init__(self, image, x1, y1, dlinna, vysota, *condotions):
        super().__init__(all_sprites)
        self.sound = pygame.mixer.Sound('../assets/sounds/lever_sound.mp3')
        self.sound.set_volume(0.3)
        self.conditions = condotions
        self.rect = pygame.Rect(x1, y1, dlinna, vysota)
        self.image = pygame.transform.smoothscale(load_image(f'objects/{image}'), self.rect.size)
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
        self.image = pygame.transform.smoothscale(load_image(f'objects/{image}'), self.rect.size)
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