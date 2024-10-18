import pygame

# image_path = '/data/data/com.pygametest.myapp/files/app/'  # адрес для игры в прилож андроид

clock = pygame.time.Clock()  # скорость прокручивания цикла

pygame.init()  # первым делам инициируем игру

screen = pygame.display.set_mode((580, 290))  # задаем расширенее, flags= pygame.NOFRAME(убрать рамку)
pygame.display.set_caption("Pygame test")  # название игре
icon = pygame.image.load ('images/icon.png')
pygame.display.set_icon(icon)  # установили иконку
# player
bg = pygame.image.load('images/bg.jpg')

walk_left = [
    pygame.image.load('images/player_left/pl1.png').convert_alpha(),
    pygame.image.load('images/player_left/pl2.png').convert_alpha(),
    pygame.image.load('images/player_left/pl3.png').convert_alpha(),
    pygame.image.load( 'images/player_left/pl4.png').convert_alpha(),
]

walk_right = [
    pygame.image.load('images/player_right/pr1.png').convert_alpha(),
    pygame.image.load('images/player_right/pr2.png').convert_alpha(),
    pygame.image.load('images/player_right/pr3.png').convert_alpha(),
    pygame.image.load('images/player_right/pr4.png').convert_alpha(),
]

whisper = pygame.image.load('images/whisper.png').convert_alpha()  # создаем приведение и переделываем формат
whisper_list_create = []

player_anim_count = 0
bg_x = 0

player_speed = 5  # скорость для передвижения игрока
player_x = 150  # расположение игрока
player_y = 200  # координаты игрока

is_jump = False
jump_count = 8  # высота прыжка
bg_sounds = pygame.mixer.Sound('sounds/prontera.mp3')  # запустить звук игры
bg_sounds.play()  # запуск

whisper_timer = pygame.USEREVENT + 1  # обязательно +1
pygame.time.set_timer(whisper_timer, 2500)  # таймер через 2,5 секунды появления нового привидения

label = pygame.font.Font('fonts/Roboto-BlackItalic.ttf', 40)
lose_label = label.render('Вы проиграли!', False, (193, 196, 199))
restart_label = label.render('Играть заново', False, (115, 132, 148))
restart_label_rect = restart_label.get_rect(topleft=(150, 200))

bullets_left = 5
bullet = pygame.image.load('images/bullet.png').convert_alpha()
bullets = []

gameplay = True

running = True
while running:  # цикл для постоянного обновления экрана

    screen.blit(bg, (bg_x, 0))  # запускаем картинку( координаты 0, 0)
    screen.blit(bg, (bg_x + 580, 0))  # Задний фон для динамики

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))  # рисуем квадрат вокруг игрока

        if whisper_list_create:
            for (i, el) in enumerate(whisper_list_create):
                screen.blit(whisper, el)
                el.x -= 10

                if el.x < -10:
                    whisper_list_create.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()  # нажатие кнопок
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))  # запускаем человечка + движение в лево
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 20:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 200:
            player_x += player_speed

        if not is_jump:  # прыжок
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:  # реализуем прыжок
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2  # эффект сглаживания прыжка
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x == -580:  # смещение и возврат картинки заднего фона
            bg_x = 0

        if bullets:
            for (i, el) in enumerate(bullets):  # стрельба
                screen.blit(bullet, (el.x, el.y))
                el.x += 4

                if el.x > 585:
                    bullets.pop(i)

                if whisper_list_create:  # удаление монстра
                    for (index, whisper_el) in enumerate(whisper_list_create):
                        if el.colliderect(whisper_el):
                            whisper_list_create.pop(index)
                            bullets.pop(i)


    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (150, 100))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[
            0]:  # проверка координат мышки с кнопкой
            gameplay = True
            player_x = 150
            whisper_list_create.clear()
            bullets.clear()
            bullets_left = 5

    pygame.display.update()

    for event in pygame.event.get():  # список всех событий
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()  # закрытие приложение через активные кнопки
        if event.type == whisper_timer:
            whisper_list_create.append(
                whisper.get_rect(topleft=(591, 210)))  # Рисование нового квадрата где появляется монтстр
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_b and bullets_left > 0:  # событие, которое выполняется при отпускании клавиши и выпускает потрон
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))  # запуск снаряда
            bullets_left -= 1

    clock.tick(15)  # устонавливем количество фреймов в одну секунду

"""1 и 2 занятие"""

# square = pygame.Surface((50, 170))# поверхность
# square.fill('Blue')
#
# myfont = pygame.font.Font('fonts/Roboto-BlackItalic.ttf', 40) # шрифт и размер
# text_surface = myfont.render('test', True, 'Red')# Доп хорактеристики для текста
#
# player = pygame.image.load('images/icon.png')
#
#
# running = True
# while running:# цикл для постоянного обновления экрана
#     pygame.draw.circle(screen, 'Red', (10, 7), 5)  # создаем еще один объект
#     screen.blit(square, (10, 0)) # создаем объект и указываем координаты
#     screen.blit(text_surface, (300, 100)) # dlit выводит все на экран
#     screen.blit(player, (100, 50))
#
#
#     pygame.display.update()
#
#     for event in pygame.event.get():# список всех событий
#         if event.type == pygame.QUIT:
#             running = False
#             pygame.quit() #закрытие приложение через активные кнопки
#
