import os
import pygame
import pygame_gui # это надо для кнопочек и окон диалоговых
import sys # это вот так называемые библеотеки, я их использовал
from random import choice, randrange
from screens import end_screen, start_screen # приколы из других py файлов
from classes_modules import *
from level_parser import parse_level

GRAVITY = 15 # гравитация, почему 15? По приколу


def update_collision(): # обрабатывает коллизию, на это ушло 4 дня
    global left, right, up, flag_gravity, running, fon_y, fon_x # да, да-да, да, не осуждайте
    x_dir = None # так надо, чтоб потом проверять
    go = left + right # направление, куда идёт игрок
    player.rect.x += go # игрок идёт
    if go != 0 and not flag_gravity: # анимация падения
        player.update_run()
    else:
        player.update_idle() # анимация спокойствия
    if go > 0: # если бежит вправо, то картинка вправо
        if player.orientation < 0:
            player.image = pygame.transform.flip(player.image, True, False)
            player.orientation = 1
    elif go < 0: # влево
        if player.orientation > 0:
            player.image = pygame.transform.flip(player.image, True, False)
            player.orientation = -1
    if objects: # проход по объектам и проверка коллизии с ними
        for object_ in objects:
            if player.mask.overlap(object_.mask, # если касается объекта, то идёт проверка
                                   (object_.rect.x - player.rect.x, object_.rect.y - player.rect.y)):
                if isinstance(object_, Wall): # в стену не даст войти
                    player.rect.x -= go
                elif isinstance(object_, Land): # сбоку в платформы не залезть
                    if player.rect.y + player.rect.height > object_.rect.y + 1:
                        player.rect.x -= go
                elif isinstance(object_, Portal): # коллизия с порталом
                    for port in objects:
                        if isinstance(port, Portal): # поиск сопряжённого портала
                            if object_.who_id == port.my_id: # проверка id портала
                                if port.direction == 'right': # игрока выкидывает чуть дальше влево или вправо, чтобы было получше
                                    if player.mask.overlap(object_.mask, (
                                    object_.rect.x - player.rect.x - 30, object_.rect.y - player.rect.y)):
                                        x_dir = 70 # вправо на 70+
                                else:
                                    if player.mask.overlap(object_.mask, (
                                    object_.rect.x - player.rect.x + 30, object_.rect.y - player.rect.y)):
                                        x_dir = -70 # влево на 70+
                                if x_dir: # если мы провели предыдущие проверки,то должно быть
                                    x_p, y_p = (port.rect.x - player.rect.x + x_dir, player.rect.y - port.rect.y) # координаты, куда нужно всё переместить
                                    for obj in objects: # перенос и понеслось
                                        obj.rect.x = obj.rect.x - x_p
                                        obj.rect.y = obj.rect.y + y_p - player.rect.height
                                    for obj in player_objects:
                                        obj.rect.x = obj.rect.x - x_p
                                        obj.rect.y = obj.rect.y + y_p - player.rect.height
                                    exit_.rect.x = exit_.rect.x - x_p
                                    exit_.rect.y = exit_.rect.y + y_p - player.rect.height
                                    x_p //= 0.85 # вот чтобы паралакс оставался
                                    fon_x += x_p
                                    port.sound_.play() # звук портала
                                    break
    if (((exit_.rect.x + 25 <= player.rect.x <= exit_.rect.x + exit_.rect.width) and ( # если игрок зашёл в зону выхода
            exit_.rect.x <= player.rect.x + player.rect.width <= exit_.rect.x + exit_.rect.width - 25))
            and (exit_.rect.y < player.rect.y < exit_.rect.y + exit_.rect.height)):
        if all(exit_.conditions): # если все условия выполнены
            running = False
    player.rect.y += up # после огромного блока сверху, можно начать просчитывать передвижение по y
    if objects:
        for object_ in objects:
            if isinstance(object_, Land): # вот чтобы фокусы Коперфилда не происходили очень сложно и мутурно считаем где игрок, куда подвинуть
                if player.mask.overlap(object_.mask,
                                       (object_.rect.x - player.rect.x, object_.rect.y - player.rect.y - 2)):
                    if object_.rect.y <= player.rect.y <= object_.rect.y + object_.rect.height:
                        player.rect.y = object_.rect.y + object_.rect.height
                        up += 3.5 # чтобы игрок чуть-чуть завис вверху у платформы, иначе будет выглядеть так, что игрок вообще не прыгнул
                    elif player.rect.y + player.rect.height > object_.rect.y + 1: # если игрок стоит на поверхности отключаем гравитацию
                        player.rect.y = object_.rect.y - player.rect.height
                    flag_gravity = False
                    break
        else: # если там не отключилась гравитация, то она действует
            flag_gravity = True
            player.rect.y += GRAVITY
            player.update_fall() # анимация падения


def object_update(): # передвижения объектов, чтобы был эффект камеры в центре
    global fon_x, fon_y, exit_
    if player.rect.x + 1 <= camera_rect.x: # игрок не может выйти за границу камеры на экране
        player.rect.x = camera_rect.x
        fon_x += 2 # фон двигаем чуть помедленее, типа паралакс и фон далеко
        if fon_x >= 600: # если фон улетел в тартарары, возвращаем на место
            fon_x = 0
        for object_ in objects: # двигаем все платформы и стенки и т.д.
            object_.rect.x += 7
        for pl_objrect in player_objects:
            pl_objrect.rect.x += 7
        exit_.rect.x += 7

    elif player.rect.width + player.rect.x - 1 >= camera_rect.width + camera_rect.x:
        player.rect.x = camera_rect.x + camera_rect.width - player.rect.width # то же самое, что выше, но для правой границы камеры
        fon_x -= 2
        if fon_x <= -600:
            fon_x = 0
        for object_ in objects:
            object_.rect.x -= 7
        for pl_objrect in player_objects:
            pl_objrect.rect.x -= 7
        exit_.rect.x -= 7

    if player.rect.y + 1 <= camera_rect.y: # тут уже просчёт по у, но порталы не очень дружат с паралаксом по н, по этому здесь мы фон не двигаем
        player.rect.y = camera_rect.y
        for object_ in objects:
            object_.rect.y += 7
        for pl_objrect in player_objects:
            pl_objrect.rect.y += 7
        exit_.rect.y += 7

    elif player.rect.height + player.rect.y - 1 >= camera_rect.height + camera_rect.y: # нижняя граница камеры
        player.rect.y = camera_rect.y + camera_rect.height - player.rect.height
        for object_ in objects:
            object_.rect.y -= 7
        for pl_objrect in player_objects:
            pl_objrect.rect.y -= 7
        exit_.rect.y -= 7


if __name__ == '__main__':
    pygame.init() # инициализация всего

    start_screen()
    pygame.display.set_caption('Game')
    size = wight, height = 600, 600
    main_window = pygame.display.set_mode(size)
    load_screen = pygame.transform.smoothscale(load_image('fons/load_screen.png'), (600, 600)) # подгрузка экрана загрузки, чтоб не делать это каждый раз
    oleg = pygame.mixer.Sound('../assets/sounds/lever_sound.mp3') # подгружаю этот звук, просто чтоб у меня был уже готовый объект для дальнейшего
    clock_delta = pygame.time.Clock()
    clock = pygame.time.Clock()

    flag_gravity = True
    manager = pygame_gui.UIManager(size) # ui элементы вкл.
    for level in range(1, len(os.listdir('../assets/levels')) + 1): # из txt файла подгружаем уровени
        player, level_fon, level_sky, objects, player_objects, music, exit_ = parse_level(f'{level}_level') # из функции отбираем все объеты
        indic = Indicator(main_window, exit_) # рисуем кружочки в зависимости от кол-ва условий
        background = pygame.transform.smoothscale(load_image(f'fons/{level_fon}'), (wight, height)) # растягиваем задник
        bg_2 = pygame.transform.smoothscale(load_image(f'fons/{level_sky}'), (5000, 3000))

        fon_x, fon_y = 0, 0 # координаты фона
        pygame.mixer.music.load(f'../assets/sounds/fon_music/{music}') # загружаем и запускаем музыку с уровня
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()
        camera_rect = pygame.Rect((300 - 75, 300 - 40), (150, 80)) # определяем грани камеры
        running = True
        up = 0
        while running:
            # запихиваем задник
            main_window.blit(background, (fon_x, fon_y))
            main_window.blit(background, (fon_x + 600, fon_y))
            main_window.blit(background, (fon_x - 600, fon_y))
            main_window.blit(bg_2, (-2500, fon_y - 3000))
            collect = pygame.key.get_pressed() # смотрим на нажатые клавиши
            time_delta = clock_delta.tick(60) / 1000
            for event in pygame.event.get(): # если игрок нажал Х, аккуратно спрашиваем, точно ли он выйти хотел
                if event.type == pygame.QUIT:
                    confor_dialog = pygame_gui.windows.UIConfirmationDialog(
                        rect=pygame.Rect((150, 200), (300, 200)),
                        manager=manager,
                        window_title='Ало?',
                        action_long_desc='Куда собрался?',
                        action_short_name='Ок',
                        blocking=True
                    )

                if event.type == pygame.KEYDOWN: # проверка клавиш
                    if event.key == pygame.K_w or event.key == pygame.K_SPACE: # на пробел прыжок, но только если игрок не пересекается ни с чем
                        if any(player.mask.overlap(land.mask,
                                                   (land.rect.x - player.rect.x, land.rect.y - player.rect.y - 2)) for
                               land in objects):
                            up = -GRAVITY * 2.5 # значение прыжка
                    if event.key == pygame.K_RETURN:
                        for i in player_objects: # на enter взаимодействие
                            if ((player.rect.x + player.rect.width // 2 + 70 > i.rect.x) and
                                    (player.rect.x + player.rect.width // 2 - 70 < i.rect.x + i.rect.width) and
                                    (player.rect.y + player.rect.height // 2 > i.rect.y) and
                                    (player.rect.y + player.rect.height // 2 < i.rect.y + i.rect.height)):
                                i.touch() # взаимодействие с рычагом
                                i.switch(exit_) # анимация рычага
                                if not all(exit_.conditions): # если нажатие не решило загадку, с шансом 1/12 олег скажет что-то грустное
                                    if randrange(12) == 4:
                                        oleg.stop()
                                        oleg = pygame.mixer.Sound(f"../assets/sounds/oleg_speak/{choice(os.listdir('../assets/sounds/oleg_speak'))}")
                                        oleg.play()
                                break

                if event.type == pygame.USEREVENT: # если игрок согласился выйти, закрываем программу
                    if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                        pygame.quit()
                        sys.exit()
                manager.process_events(event)
            if collect[pygame.K_a]: # обработка wasd, понимаем куда игрок хочет двигаться
                left = -7
            else:
                left = 0
            if collect[pygame.K_d]:
                right = 7
            else:
                right = 0

            update_collision() # функция коллизии

            object_update() # передвижение объектов
            if up < 0: # уменьшаем прыжок со временем
                up += 1
            manager.update(time_delta) # обновление экрана
            all_sprites.draw(main_window)
            manager.draw_ui(main_window)
            indic.draw_circles()

            pygame.display.update()
            clock.tick(60)
        pygame.mixer.music.stop() # останавливаем музыку
        main_window.blit(load_screen, (0, 0)) # очищаем экран и списки объектов
        pygame.display.update()
        for sprite in all_sprites:
            all_sprites.remove(sprite)
        objects.clear()
        player_objects.clear()

    end_screen() # экран конца игры
