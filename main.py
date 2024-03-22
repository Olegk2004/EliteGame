# Заготовка для игры
import pygame, sys
from settings import *
from math import sqrt
from IPython.display import clear_output
from galaxy import Galaxy
from player import Player
from galaxy_plot import create_plot
from galaxy_map import *
import galaxy_map
from pirate import Pirate
import numpy as np

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
        ms = 1

        ration = 0 # Для полоски
        clock = pygame.time.Clock() #Для контроля частоты кадров
        new_galaxy.create_matches()
        player = Player(new_galaxy)
        pirate = Pirate(new_galaxy)
        # create_plot(new_galaxy)  # Изображение графа связей планет
        pygame.mixer.music.play(-1)
        music_is_muted = False
        running = True
        while running:

            map = Map(new_galaxy, player, pirate)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    coord = event.pos
                    cheked_mouse = map.check_mouse(coord)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Если нажата левая кнопка мыши

                        click_pos = pygame.mouse.get_pos()

                        clicked_planet = map.check_click(click_pos)
                        if clicked_planet:
                            ms -= 1

                            player.bar_save = player.fuel

                            a = player.jump(clicked_planet)


                            ration = 100




                            pirate.wish()
                            b = pirate.jump(pirate.wanna_visit)
                            available = new_galaxy.matches[player.current_planet]
                            if player.current_planet.gold_planet != 0 and ms < 2:
                                player.current_planet.gold_planet = 0
                                pygame.mixer.music.load('extra_music.mp3')  # Секретная музыка
                                ms += 6
                                pygame.mixer.music.set_volume(0.5)
                                pygame.mixer.music.play(-1)

                            elif player.current_planet.gold_planet != 0:
                                ms += 6
                            else:
                                if ms == 1:
                                    pygame.mixer.music.load('elite_game_cbl_ambient.wav')  # Секретная музыка
                                    ms = 0
                                    pygame.mixer.music.set_volume(0.5)
                                    pygame.mixer.music.play(-1)

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
            map.draw(self.screen, player.fuel, ration, cheked_mouse)
            ration -= 1

            pygame.display.update()
            clock.tick(FPS)# Частота кадров


if __name__ == '__main__':
    game = Game()
    game.run()
