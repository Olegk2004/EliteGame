import pygame
import galaxy
import math
import system_generator
import plansys
from math import sqrt
from settings import *


class Planet(pygame.sprite.Sprite):
    def __init__(self, image, pos, radius):
        super().__init__()
        self.pos = pos
        self.radius = radius
        self.image = image
        self.image = pygame.transform.scale(self.image, (radius * 3, radius * 3))
        self.rect = self.image.get_rect(center=pos)


class Map:
    def __init__(self, galaxy, player):
        self.galaxy = galaxy
        self.player = player
        self.all_sprites = pygame.sprite.Group()
        self.map_screen = pygame.surface.Surface((MAP_WIDTH, MAP_HEIGHT))
        self.border = pygame.surface.Surface((SCREEN_WIDTH - MAP_WIDTH, SCREEN_HEIGHT))  # Для работы с областью спарва
        self.rect = self.map_screen.get_rect()

    def distance_to(self, destination_planet):
        return int(4 * sqrt(
            (self.player.current_planet.x - destination_planet.x) * (
                        self.player.current_planet.x - destination_planet.x) + (
                        self.player.current_planet.y - destination_planet.y) * (
                    self.player.current_planet.y - destination_planet.y) / 4))

    # self.systems = galaxy.systems
    def draw(self, surface, fuel, ration, cheked_mouse):
        len_of_bar = fuel * 0.2  # Нормировка длины полоски

        if self.player.fuel > self.player.fuel_const:
            const_len_of_bar = self.player.fuel * 0.2  # Расширяет основную шкалу топлива, если топливо стало больше, чем было изначально(можно, конено, ограничить всё нововедённой переменной)
            des_of_bar_save = self.player.fuel * 0.2
            self.player.fuel_const = self.player.fuel

        else:
            const_len_of_bar = self.player.fuel_const * 0.2  # Постоянная длина синих границ полоски
            des_of_bar_save = self.player.bar_save * 0.2  # Для сохранения координаты, до куда в прошлый раз коцнулась полоска
        len_of_got_bar = 0
        len_of_spent_bar = (des_of_bar_save - len_of_bar)  # Длина коцки
        if len_of_spent_bar < 0:
            len_of_spent_bar = 0
            len_of_got_bar = len_of_bar - des_of_bar_save
        for system in self.galaxy.systems:
            if system == self.player.current_planet:  # если это текущая планета игрока, то рисуем одним цветом
                planet_sprite = Planet(STANDART_PLANET_IMAGE, (system.x, system.y), 5)
            elif system in self.player.visited_planets:  # если это посещенная планета, то другим
                planet_sprite = Planet(STANDART_PLANET_IMAGE, (system.x, system.y), 3)
            else:
                if system.gold_planet != 0:
                    planet_sprite = Planet(SUPER_FUEL_PLANET_IMAGE, (system.x, system.y), 4)

                elif system.fuel_station_value != 0:
                    planet_sprite = Planet(FUEL_STATION_PLANET_IMAGE, (system.x, system.y), 3)

                else:
                    planet_sprite = Planet(STANDART_PLANET_IMAGE, (system.x, system.y), 3)
            self.all_sprites.add(planet_sprite)

        for match in self.galaxy.matches[self.player.current_planet]:
            pygame.draw.line(self.map_screen, EDGES_COLOR, (self.player.current_planet.x, self.player.current_planet.y),
                             (match.x, match.y), 2)
        self.all_sprites.draw(self.map_screen)
        self.all_sprites.update()
        pygame.draw.rect(self.map_screen, (255, 255, 255), self.rect, 2)

        pygame.draw.rect(self.border, (255, 255, 255), (0, 600, 300, 5), 5)  # границы полей справа, область снизу
        pygame.draw.rect(self.border, (255, 255, 255), (0, 350, 300, 5), 5)  # область по середине
        pygame.draw.rect(self.border, (255, 255, 255), (0, 0, 300, 2), 5)  # верхняя область

        pygame.draw.rect(self.border, (0, 0, 255), (3, 315, const_len_of_bar, 35), 5)  # Параметры полоски топлива
        pygame.draw.rect(self.border, (255, 0, 0), (6, 320, const_len_of_bar - 7, 25), 13)
        pygame.draw.rect(self.border, (0, 255, 0), (6, 320, len_of_bar - 7, 25), 13)

        pygame.font.init()  # инициализация текста
        my_font = pygame.font.SysFont('Comic Sans MS', 15)  # его параметры
        text_surface = my_font.render(f'У вас топлива: {self.player.fuel}, max: {MAX_FUEL_VALUE}', False,
                                      (255, 255, 255))
        text2 = my_font.render(f'Вы находитесь на планете: ', False, (255, 255, 255))
        text3 = my_font.render(f'{self.player.current_planet.name}', False, (255, 255, 255))
        text4 = my_font.render(f'Тип планеты: ', False, (255, 255, 255))
        text5 = my_font.render(f'{self.player.current_planet.type}', False, (255, 255, 255))
        text6 = my_font.render(f'Ресурсы: ', False, (255, 255, 255))
        text7 = my_font.render(f'Топливо: ', False, (255, 255, 255))
        text12 = my_font.render(f"", False, (0, 0, 0))
        text9 = my_font.render("", False, (255, 255, 255))
        text8 = my_font.render(f'{self.player.current_planet.fuel_station_value_save}', False, (255, 255, 255))
        text13 = text10 = text11 = my_font.render(f"", False, (0, 0, 0))
        text15 = my_font.render(f"Кол-во посещённых планет: {len(self.player.visited_planets)}", False, (255, 255, 255))
        if cheked_mouse in self.player.visited_planets:
            text9 = my_font.render(f'Планета : {cheked_mouse.name}', False,
                                   (255, 255, 255))  # Пошла информация о наведённой курсором планете
            # text10 = my_font.render(f'Доступные ресурсы: ', False, (255, 255, 255))
            # text11 = my_font.render(f'Топливо: {cheked_mouse.fuel_station_value}', False, (255, 255, 255))
            text12 = my_font.render(f'Необходимо топлива: {self.distance_to(cheked_mouse)}', False, (255, 255, 255))

        elif cheked_mouse in self.galaxy.matches[self.player.current_planet]:
            text13 = my_font.render(f'Неисследованная планета', False, (255, 255, 255))
            text12 = my_font.render(f'Необходимо топлива: {self.distance_to(cheked_mouse)}', False, (255, 255, 255))
        elif cheked_mouse in self.galaxy.systems:
            text13 = my_font.render(f'Неисследованная планета', False, (255, 255, 255))
            text12 = my_font.render('Необходимо топлива: неизвестно', False, (255, 255, 255))
        else:
            text9 = my_font.render("Космическое пространство", False, (255, 255, 255))
            tetx12 = text13 = text10 = text11 = my_font.render(f"", False, (0, 0, 0))

        pygame.draw.rect(self.border, (255, 255, 0),
                         (des_of_bar_save - len_of_spent_bar - 1, 320, len_of_spent_bar * int(ration) / 100, 25),
                         13)  # Анимированный расход топлива
        pygame.draw.rect(self.border, (255, 0, 255), (
        des_of_bar_save + len_of_got_bar * int(-ration) / 100 + len_of_got_bar, 320, len_of_got_bar * int(ration) / 100,
        25), 14)

        surface.blit(self.map_screen, self.rect)
        self.border.blit(text_surface, (40, 5))  # У вас топлива
        self.border.blit(text2, (40, 25))  # Вы находитесь
        self.border.blit(text3, (40, 40))
        self.border.blit(text4, (40, 65))  # Тип планеты
        self.border.blit(text5, (40, 80))
        self.border.blit(text6, (40, 105))  # Ресурсы
        self.border.blit(text7, (40, 120))
        self.border.blit(text15, (40, 140))
        self.border.blit(text8, (115, 120))
        self.border.blit(text9, (5, 375))
        self.border.blit(text10, (5, 395))
        self.border.blit(text11, (5, 415))
        self.border.blit(text12, (5, 415))
        self.border.blit(text13, (5, 395))

        surface.blit(self.border, (SCREEN_HEIGHT, 0))

    def check_click(self, click_pos):
        for planet in self.galaxy.matches[self.player.current_planet]:
            distance = ((planet.x - click_pos[0]) ** 2 + (planet.y - click_pos[
                1]) ** 2) ** 0.5  # Вычисляем расстояние между центром планеты и местом клика
            if distance < 4:  # Если клик произошел в пределах радиуса планеты
                return planet  # Возвращаем планетy
        return None

    def check_mouse(self, mouse_pos):
        for planet in self.galaxy.systems:
            distance = ((planet.x - mouse_pos[0]) ** 2 + (planet.y - mouse_pos[
                1]) ** 2) ** 0.5
            if distance < 4:  # Если курсор находится в пределах радиуса планеты
                return planet  # Возвращаем планетy
        return None
