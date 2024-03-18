import pygame
import galaxy
import math
from settings import *


class Planet(pygame.sprite.Sprite):
    def __init__(self, col, pos, radius):
        super().__init__()
        self.col = col
        self.pos = pos
        self.radius = radius
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.col, (self.radius, self.radius), self.radius)
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
    def __init__(self, galaxy, player):
        self.galaxy = galaxy
        self.player = player
        self.all_sprites = pygame.sprite.Group()

    def draw(self, surface):
        for system in self.galaxy.systems:
            if system == self.player.current_planet:  # если это текущая планета игрока, то рисуем одним цветом
                planet_sprite = Planet(CURRENT_PLANET_COLOR, (system.x, system.y), 5)
            elif system in self.player.visited_planets:  # если это посещенная планета, то другим
                planet_sprite = Planet(VISITED_PLANETS_COLOR, (system.x, system.y), 3)
            else:
                planet_sprite = Planet(UNVISITED_PLANETS_COLOR, (system.x, system.y), 3)
            self.all_sprites.add(planet_sprite)

        for match in self.galaxy.matches[self.player.current_planet]:
            # edge_sprite = Edge(EDGES_COLOR, (self.player.current_planet.x, self.player.current_planet.y), (match.x, match.y), 1)
            # self.all_sprites.add(edge_sprite)
            pygame.draw.line(surface, EDGES_COLOR, (self.player.current_planet.x, self.player.current_planet.y),
                             (match.x, match.y), 1)
        self.all_sprites.draw(surface)
        '''
        for match in galaxy.matches:
            curr_x = match.x / 260 * settings.SCREEN_WIDTH + 5
            curr_y = match.y / 260 * settings.SCREEN_HEIGHT + 5
            for i in galaxy.matches[match]:
                match_x = i.x / 260 * settings.SCREEN_WIDTH + 5
                match_y = i.y / 260 * settings.SCREEN_HEIGHT + 5
                pygame.draw.line(surface, settings.EDGES_COLOR, (curr_x, curr_y), (match_x, match_y), 1)
        '''

    def check_click(self, click_pos):
        for planet in self.galaxy.matches[self.player.current_planet]:
            distance = ((planet.x - click_pos[0])**2 + (planet.y - click_pos[1])**2)**0.5  # Вычисляем расстояние между центром планеты и местом клика
            if distance < 4:  # Если клик произошел в пределах радиуса планеты
                return planet  # Возвращаем имя планеты
        return None
