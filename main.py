# Заготовка для игры
import pygame, sys
from settings import *

from IPython.display import clear_output
from galaxy import Galaxy
from player import Player
from galaxy_plot import create_plot
from galaxy_map import *
import galaxy_map


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
                            player.jump(clicked_planet)
                            self.screen.fill((0, 0, 0))
            map.all_sprites.update()
            map.draw(self.screen)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
