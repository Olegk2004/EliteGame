import pygame
import galaxy
import math
import system_generator
from settings import *


class Planet(pygame.sprite.Sprite):
    def __init__(self, image, pos, radius):
        super().__init__()
        self.pos = pos
        self.radius = radius
        self.image = image
        self.image = pygame.transform.scale(self.image, (radius * 3, radius * 3))
        self.rect = self.image.get_rect(center=pos)


'''
class Edge(pygame.sprite.Sprite):
    def __init__(self, col, pos_start, pos_end, width):
        super().__init__()
        self.col = col
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.width = width
        dx = self.pos_end[0] - self.pos_start[0]
        dy = self.pos_end[1] - self.pos_start[1]
        length = int((dx ** 2 + dy ** 2) ** 0.5)
        self.image = pygame.Surface((abs(dx), abs(dy)), pygame.SRCALPHA)
        if pos_start[0] <= pos_end[0] and pos_start[1] <= pos_end[1]:
            pygame.draw.line(self.image, self.col, (0, 0), (abs(dx), abs(dy)), self.width)
            self.rect = self.image.get_rect(topleft=pos_start)
        elif pos_start[0] <= pos_end[0] and pos_start[1] >= pos_end[1]:
            pygame.draw.line(self.image, self.col, (0, abs(dx)), (abs(dx), 0), self.width)
            self.rect = self.image.get_rect(topright=pos_end)
        elif pos_start[0] >= pos_end[0] and pos_start[1] <= pos_end[1]:
            pygame.draw.line(self.image, self.col, (0, abs(dx)), (abs(dx), 0), self.width)
            self.rect = self.image.get_rect(topright=pos_start)
        elif pos_start[0] >= pos_end[0] and pos_start[1] >= pos_end[1]:
            pygame.draw.line(self.image, self.col, (0, 0), (abs(dx), abs(dy)), self.width)
            self.rect = self.image.get_rect(topleft=pos_end)
'''


class Map:
    def __init__(self, galaxy, player, pirate):
        self.galaxy = galaxy
        self.player = player
        self.pirate = pirate
        self.all_sprites = pygame.sprite.Group()
        self.map_screen = pygame.surface.Surface((MAP_WIDTH, MAP_HEIGHT))
        self.rect = self.map_screen.get_rect()

    # self.systems = galaxy.systems
    def draw(self, surface):

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
            # edge_sprite = Edge(EDGES_COLOR, (self.player.current_planet.x, self.player.current_planet.y), (match.x, match.y), 1)
            # self.all_sprites.add(edge_sprite)
            pygame.draw.line(self.map_screen, EDGES_COLOR, (self.player.current_planet.x, self.player.current_planet.y),
                             (match.x, match.y), 1)
        self.all_sprites.draw(self.map_screen)
        surface.blit(self.map_screen, self.rect)

    def check_click(self, click_pos):
        for planet in self.galaxy.matches[self.player.current_planet]:
            distance = ((planet.x - click_pos[0]) ** 2 + (planet.y - click_pos[
                1]) ** 2) ** 0.5  # Вычисляем расстояние между центром планеты и местом клика
            if distance < 4:  # Если клик произошел в пределах радиуса планеты
                return planet  # Возвращаем имя планеты
        return None
