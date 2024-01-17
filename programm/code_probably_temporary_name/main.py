import pygame
import pygame_gui
import sys
from screens import end_screen, start_screen
from classes_modules import *
from level_parser import parse_level, portals

GRAVITY = 15




def update_collision():
    global left, right, up, flag_gravity, runnning, fon_y, fon_x
    x_dir = None
    go = left + right
    player.rect.x += go
    if go != 0 and not flag_gravity:
        player.update_run()
    else:
        player.update_idle()
    if go > 0:
        if player.orientation < 0:
            player.image = pygame.transform.flip(player.image, True, False)
            player.orientation = 1
    elif go < 0:
        if player.orientation > 0:
            player.image = pygame.transform.flip(player.image, True, False)
            player.orientation = -1
    if objects:
        for object_ in objects:
            if player.mask.overlap(object_.mask,
                                   (object_.rect.x - player.rect.x, object_.rect.y - player.rect.y)):
                if isinstance(object_, Wall):
                    player.rect.x -= go
                elif isinstance(object_, Land):
                    if player.rect.y + player.rect.height > object_.rect.y + 1:
                        player.rect.x -= go
                elif isinstance(object_, Portal):
                    for port in objects:
                        if isinstance(port, Portal):
                            if object_.who_id == port.my_id:
                                if port.direction == 'right':
                                    if player.mask.overlap(object_.mask,(object_.rect.x - player.rect.x - 30,object_.rect.y - player.rect.y)):
                                        x_dir = 70
                                else:
                                    if player.mask.overlap(object_.mask,(object_.rect.x - player.rect.x + 30,object_.rect.y - player.rect.y)):
                                        x_dir = -70
                                if x_dir:
                                    x_p, y_p = (port.rect.x - player.rect.x + x_dir, player.rect.y - port.rect.y)

                                    for obj in objects:
                                        obj.rect.x = obj.rect.x - x_p
                                        obj.rect.y = obj.rect.y + y_p - player.rect.height
                                    for obj in player_objects:
                                        obj.rect.x = obj.rect.x - x_p
                                        obj.rect.y = obj.rect.y + y_p - player.rect.height
                                    exit_.rect.x = exit_.rect.x - x_p
                                    exit_.rect.y = exit_.rect.y + y_p - player.rect.height
                                    x_p //= 0.85
                                    fon_x += x_p
                                    port.sound_.play()
                                    break
    if (((exit_.rect.x + 40 <= player.rect.x <= exit_.rect.x + exit_.rect.width) and (
            exit_.rect.x <= player.rect.x + player.rect.width <= exit_.rect.x + exit_.rect.width - 40))
            and (exit_.rect.y < player.rect.y < exit_.rect.y + exit_.rect.height)):
        if all(exit_.conditions):
            runnning = False
    player.rect.y += up
    if objects:
        for object_ in objects:
            if isinstance(object_, Land):
                if player.mask.overlap(object_.mask,
                                       (object_.rect.x - player.rect.x, object_.rect.y - player.rect.y - 2)):
                    if object_.rect.y <= player.rect.y <= object_.rect.y + object_.rect.height:
                        player.rect.y = object_.rect.y + object_.rect.height
                        up += 3.5
                    elif player.rect.y + player.rect.height > object_.rect.y + 1:
                        player.rect.y = object_.rect.y - player.rect.height
                    flag_gravity = False
                    break
        else:
            flag_gravity = True
            player.rect.y += GRAVITY
            player.update_fall()


def object_update():
    global fon_x, fon_y, exit_
    if player.rect.x + 1 <= camera_rect.x:
        player.rect.x = camera_rect.x
        fon_x += 2
        if fon_x >= 600:
            fon_x = 0
        for object_ in objects:
            object_.rect.x += 7
        for pl_objrect in player_objects:
            pl_objrect.rect.x += 7
        exit_.rect.x += 7

    elif player.rect.width + player.rect.x - 1 >= camera_rect.width + camera_rect.x:
        player.rect.x = camera_rect.x + camera_rect.width - player.rect.width
        fon_x -= 2
        if fon_x <= -600:
            fon_x = 0
        for object_ in objects:
            object_.rect.x -= 7
        for pl_objrect in player_objects:
            pl_objrect.rect.x -= 7
        exit_.rect.x -= 7

    if player.rect.y + 1 <= camera_rect.y:
        player.rect.y = camera_rect.y
        for object_ in objects:
            object_.rect.y += 7
        for pl_objrect in player_objects:
            pl_objrect.rect.y += 7
        exit_.rect.y += 7

    elif player.rect.height + player.rect.y - 1 >= camera_rect.height + camera_rect.y:
        player.rect.y = camera_rect.y + camera_rect.height - player.rect.height
        for object_ in objects:
            object_.rect.y -= 7
        for pl_objrect in player_objects:
            pl_objrect.rect.y -= 7
        exit_.rect.y -= 7


if __name__ == '__main__':
    pygame.init()

    start_screen()
    pygame.display.set_caption('Game')
    size = wight, height = 600, 600
    main_window = pygame.display.set_mode(size)

    clock_delta = pygame.time.Clock()
    clock = pygame.time.Clock()

    flag_gravity = True
    manager = pygame_gui.UIManager(size)
    for level in range(2, 3):
        player, level_fon, level_sky, objects, player_objects, music, exit_ = parse_level(f'{level}_level')
        indic = Indicator(main_window, exit_)
        background = pygame.transform.smoothscale(load_image(f'fons/{level_fon}'), (wight, height))
        background2 = pygame.transform.smoothscale(load_image(f'fons/{level_sky}'), (5000, 3000))
        fon_x, fon_y = 0, 0
        pygame.mixer.music.load(f'../assets/sounds/fon_music/{music}')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()
        camera_rect = pygame.Rect((300 - 75, 300 - 40), (150, 80))
        runnning = True
        up = 0
        while runnning:
            main_window.blit(background, (fon_x, fon_y))
            main_window.blit(background, (fon_x + 600, fon_y))
            main_window.blit(background, (fon_x - 600, fon_y))
            main_window.blit(background2, (-2500, fon_y - 3000))
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
                            up = -GRAVITY * 2.5
                    if event.key == pygame.K_RETURN:
                        for i in player_objects:
                            if ((player.rect.x + player.rect.width // 2 + 70 > i.rect.x) and
                                    (player.rect.x + player.rect.width // 2 - 70 < i.rect.x + i.rect.width) and
                                    (player.rect.y + player.rect.height // 2 > i.rect.y) and
                                    (player.rect.y + player.rect.height // 2 < i.rect.y + i.rect.height)):
                                i.touch()
                                i.switch(exit_)

                                break

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                        pygame.quit()
                        exit()
                manager.process_events(event)
            if collect[pygame.K_a]:
                left = -7
            else:
                left = 0
            if collect[pygame.K_d]:
                right = 7
            else:
                right = 0

            update_collision()

            object_update()

            if up < 0:
                up += 1
            manager.update(time_delta)
            all_sprites.draw(main_window)
            manager.draw_ui(main_window)
            indic.draw_circles()
            pygame.display.update()
            clock.tick(60)
        main_window.fill(pygame.Color('white'))
        for sprite in all_sprites:
            all_sprites.remove(sprite)
        objects.clear()
        player_objects.clear()
    end_screen()