import pygame
import pygame_gui
import sys
from classes_modules import *
from level_parser import parse_level

GRAVITY = 15


def start_screen():
    pygame.display.set_caption('Start menu')
    size = wight, height = 800, 600
    menu_surface = pygame.display.set_mode(size)
    manager = pygame_gui.UIManager(size)
    intro_text = ["Я дам вам",
                  "игру про",
                  "Олега Тинькофф", ]
    font = pygame.font.Font(None, 30)
    fon = pygame.transform.scale(load_image('fons/menu_fon.jpg'), (wight, height))
    menu_surface.blit(fon, (0, 0))
    run = True
    start_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((100, 400), (100, 50)),
        text='Start',
        manager=manager
    )
    clock1 = pygame.time.Clock()

    while run:
        time_delta1 = clock1.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((300, 200), (300, 200)),
                    manager=manager,
                    window_title='Ало?',
                    action_long_desc='Куда собрался?',
                    action_short_name='Ок',
                    blocking=True
                )
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    pygame.quit()
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_button:
                        start_button.hide()
                        return 0
            manager.process_events(event)
        manager.update(time_delta1)
        menu_surface.blit(fon, (0, 0))
        text_coord = 100
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 60 - len(line) * 4
            text_coord += intro_rect.height
            menu_surface.blit(string_rendered, intro_rect)
        manager.draw_ui(menu_surface)
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()

    start_screen()

    pygame.display.set_caption('Game')
    size = wight, height = 600, 600
    main_window = pygame.display.set_mode(size)

    clock_delta = pygame.time.Clock()
    clock = pygame.time.Clock()

    gravity_flag = True

    manager = pygame_gui.UIManager(size)

    player, level_fon, objects = parse_level('1st_level')

    background = pygame.transform.scale(load_image(f'fons/{level_fon}'), (wight, height))
    fon_x, fon_y = 0, -30

    camera_rect = pygame.Rect((300 - 75, 0), (150, 600))
    runnning = True
    up = 0
    while runnning:
        main_window.blit(background, (fon_x, fon_y))
        main_window.blit(background, (fon_x + 600, fon_y))
        main_window.blit(background, (fon_x - 600, fon_y))
        collect = pygame.key.get_pressed()
        time_delta = clock_delta.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confor_dialog = pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((150, 200), (300, 200)),
                    manager=manager,
                    window_title='Ало?',
                    action_long_desc='Куда собрался?',
                    action_short_name='Ок',
                    blocking=True
                )

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                    if any(player.mask.overlap(land.mask,
                                               (land.rect.x - player.rect.x, land.rect.y - player.rect.y - 2)) for
                           land in objects):
                        up = -GRAVITY * 2

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    pygame.quit()
                    exit()

            manager.process_events(event)
        if collect[pygame.K_a]:
            left = -10
        else:
            left = 0
        if collect[pygame.K_d]:
            right = 10
        else:
            right = 0

        player.rect.x += left + right
        player.rect.y += up

        if objects:
            for object_ in objects:
                if isinstance(object_, Wall):
                    if player.mask.overlap(object_.mask, (object_.rect.x - player.rect.x, object_.rect.y - player.rect.y)):
                        player.rect.x -= left + right
                elif isinstance(object_, Land):
                    if player.mask.overlap(object_.mask, (object_.rect.x - player.rect.x, object_.rect.y - player.rect.y)):
                        if player.rect.y + player.rect.height > object_.rect.y:
                            player.rect.x -= left + right
                        if object_.rect.y <= player.rect.y <= object_.rect.y + object_.rect.height:
                            print(object_.rect.y + object_.rect.height, player.rect.y)
                            player.rect.y = object_.rect.y + object_.rect.height
                            gravity_flag = False
                            up = 0
        if not any(
                player.mask.overlap(land.mask, (land.rect.x - player.rect.x, land.rect.y - player.rect.y - 1)) for
                land in objects):
            player.rect.y += GRAVITY
            gravity_flag = True
        else:
            for i in objects:
                if isinstance(i, Land) and gravity_flag:
                    if player.mask.overlap(i.mask, (i.rect.x - player.rect.x, i.rect.y - player.rect.y + 1)):
                        print('gravity_collision_detect')
                        player.rect.y = i.rect.y - player.rect.height

        if player.rect.x + 1 <= camera_rect.x:
            player.rect.x = camera_rect.x
            fon_x += 1
            if fon_x >= 600:
                fon_x = 0
            for object_ in objects:
                object_.rect.x += 10

        elif player.rect.width + player.rect.x - 1 >= camera_rect.width + camera_rect.x:
            player.rect.x = camera_rect.x + camera_rect.width - player.rect.width
            fon_x -= 1
            if fon_x <= -600:
                fon_x = 0
            for object_ in objects:
                object_.rect.x -= 10



        if up < 0:
            up += 1
        manager.update(time_delta)
        all_sprites.draw(main_window)
        manager.draw_ui(main_window)
        pygame.display.update()
        clock.tick(40)
