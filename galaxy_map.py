import pygame
import galaxy
import math
import system_generator
from scipy.spatial import Voronoi
from settings import *
from debug import debug


class Planet(pygame.sprite.Sprite):
    def __init__(self, image, pos, radius):
        super().__init__()
        self.pos = pos
        self.radius = radius
        self.image = image
        self.image = pygame.transform.scale(self.image, (radius * 3, radius * 3))
        self.rect = self.image.get_rect(center=pos)


class Map:
    def __init__(self, galaxy, player, pirate):
        self.galaxy = galaxy
        self.player = player
        self.pirate = pirate
        self.all_sprites = pygame.sprite.Group()
        self.map_screen = pygame.surface.Surface((MAP_WIDTH, MAP_HEIGHT))
        self.rect = self.map_screen.get_rect()

    def draw(self, surface):
        self.draw_voronoi_segments(self.map_screen)
        for system in self.galaxy.systems:
            if system == self.player.current_planet:  # если это текущая планета игрока, то рисуем одним цветом
                if system in self.galaxy.capitals:
                    planet_sprite = Planet(CAPITAL_PLANET_IMAGE, (system.x, system.y), 5)
                else:
                    planet_sprite = Planet(CURRENT_PLANET_IMAGE, (system.x, system.y), 5)
            else:
                # Если планета золотая/c заправкой и при этом является столицей,
                # она будет помечена просто как столица (потом доработаем, когда больше запаримся со спрайтами)
                if system in self.galaxy.capitals:
                    planet_sprite = Planet(CAPITAL_PLANET_IMAGE, (system.x, system.y), 3)
                elif system.gold_planet != 0:
                    planet_sprite = Planet(SUPER_FUEL_PLANET_IMAGE, (system.x, system.y), 4)
                elif system.fuel_station_value != 0:
                    planet_sprite = Planet(FUEL_STATION_PLANET_IMAGE, (system.x, system.y), 3)
                else:
                    planet_sprite = Planet(STANDARD_PLANET_IMAGE, (system.x, system.y), 3)
            self.all_sprites.add(planet_sprite)

        for match in self.galaxy.matches[self.player.current_planet]:
            pygame.draw.line(self.map_screen, EDGES_COLOR, (self.player.current_planet.x, self.player.current_planet.y),
                             (match.x, match.y), 1)
        self.all_sprites.draw(self.map_screen)
        pygame.draw.rect(self.map_screen, (255, 255, 255), self.rect, 2)
        surface.blit(self.map_screen, self.rect)

    def draw_voronoi_segments(self, surface):
        vor = Voronoi([i.pos for i in self.galaxy.capitals])
        # Рисование границ ячеек
        for i in range(len(vor.ridge_vertices)):
            ridge = vor.ridge_vertices[i]
            if all(v >= 0 for v in ridge):
                pygame.draw.line(surface, (255, 255, 255), vor.vertices[ridge[0]], vor.vertices[ridge[1]])

            elif ridge[0] >= 0 and ridge[1] == -1:
                # Если одна вершина бесконечна, рисуем линию к краю экрана
                x0, y0 = vor.vertices[ridge[0]]
                x1, y1 = vor.vertices[vor.ridge_vertices[i][0]]
                dx = x1 - x0
                dy = y1 - y0
                if dx == 0:
                    x = x0 if x0 < MAP_WIDTH // 2 else MAP_WIDTH
                    y = 0 if y0 < MAP_HEIGHT // 2 else MAP_HEIGHT
                elif dy == 0:
                    x = 0 if x0 < MAP_WIDTH // 2 else MAP_WIDTH
                    y = y0 if y0 < MAP_HEIGHT // 2 else MAP_HEIGHT
                else:
                    slope = dy / dx
                    if abs(slope) * MAP_WIDTH > MAP_HEIGHT:
                        y = 0 if y0 < MAP_HEIGHT // 2 else MAP_HEIGHT
                        x = (y - y0) / slope + x0
                    else:
                        x = 0 if x0 < MAP_WIDTH // 2 else MAP_WIDTH
                        y = slope * (x - x0) + y0
                pygame.draw.line(surface, (255, 255, 255), (x0, y0), (x, y))
                
            elif ridge[0] == -1 and ridge[1] >= 0:
                # Если другая вершина бесконечна, рисуем линию к краю экрана
                x0, y0 = vor.vertices[ridge[1]]
                x1, y1 = vor.vertices[vor.ridge_vertices[i][1]]
                dx = x1 - x0
                dy = y1 - y0
                if dx == 0:
                    x = x0 if x0 < MAP_WIDTH // 2 else MAP_WIDTH
                    y = 0 if y0 < MAP_HEIGHT // 2 else MAP_HEIGHT
                elif dy == 0:
                    x = 0 if x0 < MAP_WIDTH // 2 else MAP_WIDTH
                    y = y0 if y0 < MAP_HEIGHT // 2 else MAP_HEIGHT
                else:
                    slope = dy / dx
                    if abs(slope) * MAP_WIDTH > MAP_HEIGHT:
                        y = 0 if y0 < MAP_HEIGHT // 2 else MAP_HEIGHT
                        x = (y - y0) / slope + x0
                    else:
                        x = 0 if x0 < MAP_WIDTH // 2 else MAP_WIDTH
                        y = slope * (x - x0) + y0
                pygame.draw.line(surface, (255, 255, 255), (x0, y0), (x, y))

    def check_click(self, click_pos):
        for planet in self.galaxy.matches[self.player.current_planet]:
            distance = ((planet.x - click_pos[0]) ** 2 + (planet.y - click_pos[
                1]) ** 2) ** 0.5  # Вычисляем расстояние между центром планеты и местом клика
            if distance < 4:  # Если клик произошел в пределах радиуса планеты
                return planet  # Возвращаем имя планеты
        return None
