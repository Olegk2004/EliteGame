# Заготовка для игры
import pygame, sys
from settings import *

from IPython.display import clear_output
from galaxy import Galaxy
from player import Player
from galaxy_plot import create_plot
import galaxy_map


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Super Elite Game")

    def run(self):
        new_galaxy = Galaxy(0x5A4A, 0x0248, 0xB753)
        new_galaxy.make_systems()
        new_galaxy.create_matches()
        player = Player(new_galaxy)
        create_plot(new_galaxy)
        galaxy_map.draw(new_galaxy, player, self.screen)

        running = True
        while running:

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Если нажата левая кнопка мыши
                        click_pos = pygame.mouse.get_pos()
                        clicked_planet = galaxy_map.check_click(click_pos, player, new_galaxy)
                        if clicked_planet:
                            player.jump(clicked_planet)
                            self.screen.fill((0, 0, 0))
                            galaxy_map.draw(new_galaxy, player, self.screen)



if __name__ == '__main__':
    game = Game()
    game.run()
