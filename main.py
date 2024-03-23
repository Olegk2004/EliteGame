# Заготовка для игры
import pygame, sys
from settings import *
from math import sqrt
from IPython.display import clear_output
from galaxy import Galaxy
from player import Player
from galaxy_map import *
from debug import debug
from planet_map import PlanetMap

import galaxy_map
import numpy as np


class Game:
    def __init__(self):
        pygame.init()

        # Работа с музыкой
        pygame.mixer.init()
        pygame.mixer.music.load('Music/elite_game_cbl_ambient.wav')  # Загрузка аудиофайла для фоновой музыки
        pygame.mixer.music.set_volume(0.5)

        # Работа с экраном
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Установка параметров окна
        pygame.display.set_caption("Super Elite Game")

    def run(self):
        # Работа с галактикой
        new_galaxy = Galaxy(0x5A4A, 0x0248, 0xB753)  # Создаем галактику с определенным сидом
        new_galaxy.make_systems()  # создаем планеты в галактике
        new_galaxy.create_matches()  # определяем для каждой планеты список доступных для прыжка

        # Для полоски
        ration = 0

        # создаем игрока
        player = Player(new_galaxy)
        # игрок пока никак не отображается, однако он нужен для отображения текущей планеты, запаса топлива и т.д.

        # Запускаем музыку
        pygame.mixer.music.play(-1)
        music_is_muted = False  # изначально музыка играет, чтобы ее выключить надо нажать "m"
        music_mode = "standart"  # переменная определяющая какой трек сейчас играет

        # Запуск цикла обновления игры, который остановится только когда пользователь выйдет из игры
        running = True
        while running:

            # создаем карты космоса и планеты
            planet_map = PlanetMap(player.current_planet)
            galaxy_map = Map(new_galaxy, player)

            # цикл обработки событий (нажатие на клавиши и мышка)
            for event in pygame.event.get():

                if event.type == pygame.QUIT:  # если нажали на красный крестик игра заканчивается
                    running = False
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:  # Нажатие кнопки мыши
                    if event.button == 1:  # Если нажата левая кнопка мыши

                        click_pos = pygame.mouse.get_pos()  # получаем координаты курсора
                        clicked_planet = galaxy_map.check_click(click_pos)  # проверяем находится ли курсор на планете

                        if clicked_planet:  # если курсор на планете

                            player.bar_save = player.fuel
                            player.jump(clicked_planet)  # совершаем прыжок

                            ration = 100

                            if player.current_planet.gold_planet != 0:  # если мы на золотой планете
                                player.current_planet.gold_planet = 0  # делаем планету обычной
                                pygame.mixer.music.load('Music/extra_music2.mp3')  # Играем секретную музыку
                                pygame.mixer.music.set_volume(0.5)
                                pygame.mixer.music.play(-1)
                                music_mode = "secret"

                            else:
                                if music_mode == "secret":  # если мы ушли с золотой планеты, запускается обычная музыка
                                    pygame.mixer.music.load('Music/elite_game_cbl_ambient.wav')
                                    pygame.mixer.music.set_volume(0.5)
                                    pygame.mixer.music.play(-1)
                                    music_mode = "standart"

                # обработка нажатия клавиш клавиатуры
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:  # нажатие на кнопку "M" выключает/включает звук музыки
                        if music_is_muted:
                            pygame.mixer.music.set_volume(0.5)
                            music_is_muted = False
                        else:
                            pygame.mixer.music.set_volume(0)
                            music_is_muted = True
                    elif event.key == pygame.K_e:  # нажатие на кнопку "E" меняет карту космоса на карту планеты
                        if player.display_mode == "map":
                            player.display_mode = "planet"
                        else:
                            player.display_mode = "map"

            self.screen.fill((0, 0, 0))  # обновляем экран заливая всю поверхность черным цветом

            checked_mouse = galaxy_map.check_mouse(
                pygame.mouse.get_pos())  # определяем позицию мышки, чтобы передать ее в функцию draw

            if player.display_mode == "map":
                galaxy_map.draw(self.screen, player.fuel, ration, checked_mouse)
            else:
                planet_map.draw(self.screen)

            # debug(str(pygame.mouse.get_pos()))  # Прикольно да))
            ration -= 1

            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
