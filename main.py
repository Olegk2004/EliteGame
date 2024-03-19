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
from IPython.display import clear_output
def distance(a, b):
  return int(4*sqrt((a.x-b.x)*(a.x-b.x)+(a.y-b.y)*(a.y-b.y)/4))
class Game:
    def __init__(self):
        pygame.init()

        pygame.mixer.init()
        pygame.mixer.music.load('elite_game_cbl_ambient.wav')  # Загрузка аудиофайла для фоновой музыки
        pygame.mixer.music.set_volume(0.5)

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Установка параметров окна
        pygame.display.set_caption("Super Elite Game")

    def run(self):
        new_galaxy = Galaxy(0x5A4A, 0x0248, 0xB753)
        new_galaxy.make_systems()

        new_galaxy.create_matches()
        player = Player(new_galaxy)
        # create_plot(new_galaxy)  # Изображение графа связей планет
        pygame.mixer.music.play(-1)
        music_is_muted = False
        print(f"Приветствуем вас, путник! Вы находитесь на планете:{player.current_planet.name}")
        print(f"У вас топлива: {player.fuel}")
        available = new_galaxy.matches[player.current_planet]
        print("Можете прыгнуть до: ")
        for i in range(len(available)):

            print(f"{i + 1}.{available[i].name}, необходимо иметь топлива: {distance(available[i], player.current_planet)}")
        running = True
        while running:

            map = Map(new_galaxy, player)
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
                            clear_output()
                            a = player.jump(clicked_planet)
                            available = new_galaxy.matches[player.current_planet]
                            if not a:
                                print("\n" * 2)
                                print(f"Вы не можете прыгнуть до планеты {clicked_planet.name}, вам не хватает топлива!")
                                print("\n" * 2)
                            else:
                                print("\n" * 10)
                                print(f"Вы находитесь на планете:{player.current_planet.name}")
                                if player.current_planet.flag != 0: #Флаг, что есть заправка
                                    print(f"Вау, здесь етсь заправка, вы заправились на {player.current_planet.fuel_station_value_save} топлива")
                                if player.current_planet.Flag != 0:#Флаг, что есть pirates
                                    print(f"Опа, здесь оказались пираты, они отняли у вас: {player.current_planet.pirates_value_save} топлива, а также попортили лицо")
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

            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
