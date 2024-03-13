# Заготовка для игры
import pygame, sys
from settings import *

from IPython.display import clear_output
from galaxy import Galaxy
from player import Player
from galaxy_plot import create_plot


class Game:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Super Elite Game")

    def run(self):
        new_galaxy = Galaxy(0x5A4A, 0x0248, 0xB753)
        new_galaxy.make_systems()
        new_galaxy.create_matches()
        player = Player(new_galaxy)
        create_plot(new_galaxy)

        running = True
        while running:

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
            # Функция для запуска очередного "цикла" игрового процесса, я хз пока куда это положить, поэтому будет здесь
            print(f"Вы находитесь на планете:{player.current_planet.name}")
            print(f"На вас напали космические пираты! У вас отняли {player.current_planet.pirates_value} литра топлива.")
            print(
                f"Вы обнаружили заправочную станцию! Вы заправились на {player.current_planet.fuel_station_value} литра топлива.")
            player.fuel -= player.current_planet.pirates_value  # уменьшаем количество топлива на то, которое у нас отобрали пираты
            player.fuel += player.current_planet.fuel_station_value  # увеличиваем количество топлива на то, что мы нашли на станции
            print(f"У вас {player.fuel} литров топлива")
            print(f"вы можете прыгнуть на планеты:")
            available = player.galaxy.matches[player.current_planet]  # список планет, на которые мы можем допрыгнуть с текущей
            available_planets = {}  # словарь чтобы пользователь мог вводить планету на которую хочет прыгнуть с помощью цифры
            for i in range(
                    len(available)):  # проходимся по номерам планет, на которые мы можем прыгнуть и добавляем под ключом
                # номера имя планеты
                available_planets[str(i)] = available[i]
                print(f"{i}. {available[i].name}, необходимо иметь топлива: {player.current_planet.distance(available[i])}")
            planet = input("Введите номер планеты на которую хотите прыгнуть: ")
            is_true = player.jump(available_planets[planet])
            clear_output(wait=False)  # пока что не работает
            if not is_true:  # если прыжок совершить невозможно
                print("У вас недостаточно топлива для данного прыжка")


if __name__ == '__main__':
    game = Game()
    game.run()
