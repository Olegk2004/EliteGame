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


class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.camera = pygame.Rect(0, 0, width, height)

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(SCREEN_WIDTH / 2)
        y = -target.rect.y + int(SCREEN_HEIGHT / 2)
        self.camera = pygame.Rect(x, y, self.width, self.height)


class Game:
    def __init__(self):
        pygame.init()
        pygame.event.set_grab(True)

        self.clock = pygame.time.Clock()
        # Работа с музыкой
        pygame.mixer.init()
        pygame.mixer.music.load('Music/elite_game_cbl_ambient.wav')  # Загрузка аудиофайла для фоновой музыки
        pygame.mixer.music.set_volume(0.5)

        # Работа с галактикой
        self.galaxy = Galaxy(0x5A4A, 0x0248, 0xB753)  # Создаем галактику с определенным сидом
        self.galaxy.make_systems()  # создаем планеты в галактике
        self.galaxy.create_matches()  # определяем для каждой планеты список доступных для прыжка

        self.camera = Camera(MAP_WIDTH, MAP_HEIGHT)

        # создаем игрока
        self.player = Player(self.galaxy)
        # игрок пока никак не отображается, однако он нужен для отображения текущей планеты, запаса топлива и т.д.

        # Работа с экраном
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Установка параметров окна
        pygame.display.set_caption("Super Elite Game")

        # Создаем объект карты планеты
        # По сути это пока один объект для всех планет, при перелете он просто перерисовывается в зависимости
        # от характеристик планеты
        self.planet_map = PlanetMap(self.player.current_planet)
        # создаем карту космоса
        self.galaxy_map = Map(self.galaxy, self.player)
    def run(self):
        # Для полоски
        ration = 0
        F = pygame.time.Clock()
        # Запускаем музыку
        pygame.mixer.music.play(-1)
        music_is_muted = False  # изначально музыка играет, чтобы ее выключить надо нажать "M"
        music_mode = "space"  # переменная определяющая какой трек сейчас играет

        # Запуск цикла обновления игры, который остановится только когда пользователь выйдет из игры
        running = True
        while running:
            # цикл обработки событий (нажатие на клавиши и мышка)
            for event in pygame.event.get():

                if event.type == pygame.QUIT:  # если нажали на красный крестик игра заканчивается
                    running = False
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:  # Нажатие кнопки мыши
                    if event.button == 1:  # Если нажата левая кнопка мыши

                        click_pos = pygame.mouse.get_pos()  # получаем координаты курсора
                        clicked_planet = self.galaxy_map.check_click(click_pos)  # проверяем находится ли курсор на планете

                        if clicked_planet or self.galaxy_map.cursor_is_within_jump_rect:  # если курсор на планете
                            if self.galaxy_map.cursor_is_within_jump_rect:
                                clicked_planet = self.galaxy_map.jump_rect_planet
                            self.player.bar_save = self.player.fuel
                            jump_done = self.player.jump(clicked_planet)  # совершаем прыжок
                            if not jump_done:
                                self.galaxy_map.out_of_fuel()
                            self.planet_map = PlanetMap(self.player.current_planet)

                            self.galaxy_map.camera_group.camera_rect = self.galaxy_map.camera_group.camera_rect_setup()
                            self.galaxy_map.camera_group.center_target_camera(self.player.current_planet)

                            ration = 100

                            if self.player.current_planet.gold_planet != 0:  # если мы на золотой планете
                                self.player.current_planet.gold_planet = 0  # делаем планету обычной
                                pygame.mixer.music.load('Music/extra_music.mp3')  # Играем секретную музыку
                                pygame.mixer.music.set_volume(0.5)
                                pygame.mixer.music.play(-1)
                                music_mode = "space_gold"

                            else:
                                if music_mode == "space_gold":  # если мы ушли с золотой планеты, запускается обычная музыка
                                    pygame.mixer.music.load('Music/elite_game_cbl_ambient.wav')
                                    pygame.mixer.music.set_volume(0.5)
                                    pygame.mixer.music.play(-1)
                                    music_mode = "space"

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
                        if self.player.display_mode == "map":
                            self.player.display_mode = "planet"
                            pygame.mixer.music.load('Music/planet_music.mp3')
                            pygame.mixer.music.set_volume(0.5)
                            pygame.mixer.music.play(-1)
                            music_mode = "planet"
                        else:
                            self.player.display_mode = "map"
                            pygame.mixer.music.load('Music/elite_game_cbl_ambient.wav')
                            pygame.mixer.music.set_volume(0.5)
                            pygame.mixer.music.play(-1)
                            music_mode = "space"
                    elif event.key == pygame.K_r:  # Нажатие на кнопку "R" возвращает зум в исходное состояние
                        self.galaxy_map.camera_group.zoom_scale = 1
                        self.galaxy_map.camera_group.camera_rect = self.galaxy_map.camera_group.camera_rect_setup()
                        self.galaxy_map.camera_group.center_target_camera(self.player.current_planet)

                if event.type == pygame.MOUSEWHEEL:
                    if pygame.mouse.get_pos()[0] < MAP_PANEL_WIDTH:
                        if event.y > 0 and self.galaxy_map.camera_group.zoom_scale - 2 < 0.085:
                            self.galaxy_map.camera_group.zoom_scale += event.y * 0.05
                        if event.y < 0 and self.galaxy_map.camera_group.zoom_scale - 0.20 > 0.085 and \
                                self.galaxy_map.camera_group.zoom_scale + event.y * 0.05 > 0.25: # )
                            self.galaxy_map.camera_group.zoom_scale += event.y * 0.05

            self.screen.fill((0, 0, 0))  # обновляем экран заливая всю поверхность черным цветом

            if self.player.display_mode == "map":
                self.galaxy_map.draw()
                checked_mouse = self.galaxy_map.check_mouse(
                    pygame.mouse.get_pos())  # определяем позицию мышки, чтобы передать ее в функцию draw
                self.galaxy_map.draw_side_panel(self.screen, self.player.fuel, ration, checked_mouse)
            else:
                dt = self.clock.tick(100) / 1000
                self.planet_map.draw(dt)

            # debug(str(pygame.mouse.get_pos()))  # Прикольно да))
            ration -= 10

            F.tick(FPS)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
