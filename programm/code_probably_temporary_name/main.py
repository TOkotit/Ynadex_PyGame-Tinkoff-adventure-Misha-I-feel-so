import pygame
import pygame_gui
import sys
import os
from classes_modules import *

GRAVITY = 15


def start_screen():
    pygame.display.set_caption('Start menu')
    size = height, wight = 800, 600
    menu_surface = pygame.display.set_mode(size)
    manager = pygame_gui.UIManager(size)
    intro_text = ["Я дам вам",
                  "игру про",
                  "Олега Тинькофф", ]
    font = pygame.font.Font(None, 30)
    fon = pygame.transform.scale(load_image('fons/menu_fon.jpg'), (height, wight))
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
                    rect=pygame.Rect((250, 200), (300, 200)),
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
    size = height, wight = 800, 600
    main_window = pygame.display.set_mode(size)
    clock_delta = pygame.time.Clock()
    clock = pygame.time.Clock()
    manager = pygame_gui.UIManager(size)
    land = Land(0, 550, 800, 600)
    background = pygame.transform.scale(load_image('fons/zaglushka.jpg'), (height, wight))
    main_window.blit(background, (0, 0))
    player = Player(40, 40)
    runnning = True
    up = 0
    while runnning:
        collect = pygame.key.get_pressed()
        time_delta = clock_delta.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confor_dialog = pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((250, 200), (300, 200)),
                    manager=manager,
                    window_title='Ало?',
                    action_long_desc='Куда собрался?',
                    action_short_name='Ок',
                    blocking=True
                )
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                    if pygame.sprite.collide_mask(player, land):
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
        if collect[pygame.K_s]:
            down = 10
        else:
            down = 0
        if collect[pygame.K_d]:
            right = 10
        else:
            right = 0
        if not pygame.sprite.collide_mask(player, land):
            player.rect.y += GRAVITY
        player.rect.x += left + right
        player.rect.y += up + down
        if up < 0:
            up += 1
        main_window.blit(background, (0, 0))
        manager.update(time_delta)
        all_sprites.draw(main_window)
        manager.draw_ui(main_window)
        pygame.display.update()
        clock.tick(20)

