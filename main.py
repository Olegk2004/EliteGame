# Заготовка для игры
import pygame, sys
from settings import *
from math import sqrt
from galaxy import Galaxy
from player import Player
from galaxy_plot import create_plot
from galaxy_map import *
from pirate import Pirate
from debug import debug
import numpy as np


def distance(a, b):
    return int(4 * sqrt((a.x - b.x) * (a.x - b.x) + (a.y - b.y) * (a.y - b.y) / 4))


class Game:
    def __init__(self):
        pygame.init()

        pygame.mixer.init()
        if np.random.rand() < 0.2:
            pygame.mixer.music.load('extra_music2.mp3')  # Секретная музыка
        else:
            pygame.mixer.music.load('elite_game_cbl_ambient.wav')  # Загрузка аудиофайла для фоновой музыки
        pygame.mixer.music.set_volume(0.5)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Установка параметров окна
        pygame.display.set_caption("Super Elite Game")

    def run(self):
        new_galaxy = Galaxy(0x5A4A, 0x0248, 0xB753)
        new_galaxy.make_systems()
        ms = 0
        new_galaxy.create_matches()
        player = Player(new_galaxy)
        pirate = Pirate(new_galaxy)
        # create_plot(new_galaxy)  # Изображение графа связей планет
        pygame.mixer.music.play(-1)
        music_is_muted = False
        print(f"Приветствуем вас, путник! Вы находитесь на планете:{player.current_planet.name}")
        print(f"У вас топлива: {player.fuel}")
        available = new_galaxy.matches[player.current_planet]
        print("Можете прыгнуть до: ")
        for i in range(len(available)):
            print(
                f"{i + 1}.{available[i].name}, необходимо иметь топлива: {distance(available[i], player.current_planet)}")

        running = True
        while running:
            map = Map(new_galaxy, player, pirate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Если нажата левая кнопка мыши

                        click_pos = pygame.mouse.get_pos()

                        clicked_planet = map.check_click(click_pos)
                        if clicked_planet:

                            a = player.jump(clicked_planet)
                            pirate.wish()
                            b = pirate.jump(pirate.wanna_visit)
                            available = new_galaxy.matches[player.current_planet]
                            if not a:
                                print("\n" * 2)
                                print(
                                    f"Вы не можете прыгнуть до планеты {clicked_planet.name}, вам не хватает топлива!")
                                print("\n" * 2)

                            else:
                                print("\n" * 10)
                                if player.current_planet.gold_planet != 0:
                                    print(f"Вы нашли 500 топлива!")
                                    pygame.mixer.music.load('extra_music.mp3')  # Секретная музыка
                                    ms = 1
                                    pygame.mixer.music.set_volume(0.5)
                                    pygame.mixer.music.play(-1)

                                else:
                                    if ms:
                                        pygame.mixer.music.load('elite_game_cbl_ambient.wav')  # Секретная музыка
                                        ms = 0
                                        pygame.mixer.music.set_volume(0.5)
                                        pygame.mixer.music.play(-1)
                                print(f"Вы находитесь на планете:{player.current_planet.name}")
                                if player.current_planet.flag != 0:  # Флаг, что есть заправка
                                    print(
                                        f"Вау, здесь есть заправка, вы заправились на {player.current_planet.fuel_station_value_save} топлива")
                                print(f"У вас топлива: {player.fuel}")
                                print("Можете прыгнуть до: ")
                                for i in range(len(available)):
                                    print(
                                        f"{i + 1}.{available[i].name}, необходимо иметь топлива: {distance(available[i], player.current_planet)}")
                            self.screen.fill((0, 0, 0))

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        if music_is_muted:
                            pygame.mixer.music.set_volume(0.5)
                            music_is_muted = False
                        else:
                            pygame.mixer.music.set_volume(0)
                            music_is_muted = True

            map.all_sprites.update()
            map.draw(self.screen)
            # debug(str(pygame.mouse.get_pos()))  # Прикольно да))

            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
