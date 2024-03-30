import pygame
import galaxy
import math
import system_generator
from scipy.spatial import Voronoi
from settings import *
from debug import debug
from planet_player import PlanetPlayer
from overlay import Overlay


class PlanetMap:
    def __init__(self, planet):
        self.planet = planet
        self.all_sprites = pygame.sprite.Group()
        self.display_surface = pygame.display.get_surface()
        self.setup()
        self.overlay = Overlay(self.display_surface, self.planet_player)

    def setup(self):
        self.planet_player = PlanetPlayer((100, 100), self.all_sprites)

    def draw(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)
        self.overlay.display()