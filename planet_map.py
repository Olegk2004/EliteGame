import pygame
import galaxy
import math
import system_generator
from scipy.spatial import Voronoi
from settings import *
from debug import debug
from planet_player import PlanetPlayer


class PlanetMap:
    def __init__(self, planet):
        self.planet = planet
        self.planet_player = None
        self.all_sprites = pygame.sprite.Group()
        self.map_screen = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect = self.map_screen.get_rect()

        self.setup()

    def setup(self):
        self.planet_player = PlanetPlayer((100, 100), self.all_sprites)

    def draw(self, surface):
        self.all_sprites.draw(self.map_screen)
        self.all_sprites.update()
        pygame.draw.rect(self.map_screen, (255, 255, 255), self.rect, 2)
        surface.blit(self.map_screen, self.rect)
