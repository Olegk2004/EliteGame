import pygame
import galaxy
import math
import system_generator
from settings import *
from debug import debug
from planet_player import PlanetPlayer
from planet_enemy import PlanetEnemy
from overlay import Overlay


class PlanetMap:
    def __init__(self, planet):
        self.planet = planet
        self.all_sprites = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.display_surface = pygame.display.get_surface()
        self.setup()

    def setup(self):
        self.planet_player = PlanetPlayer((100, 100), self.all_sprites)
        self.planet_enemies = {}
        self.enemies_overlays = {}
        for i in range(3):
            self.planet_enemies['enemy_' + str(i)] = PlanetEnemy(self.planet_player, self.bullet_group,
                                                                 self.all_sprites, (500, 100 + i * 100))
            self.enemies_overlays['enemy_' + str(i)] = Overlay(self.display_surface,
                                                               self.planet_enemies['enemy_' + str(i)])
        self.overlay = Overlay(self.display_surface, self.planet_player)

    def draw(self, dt):
        self.display_surface.fill('black')
        for sprite in sorted(self.all_sprites, key=lambda sprite: sprite.rect.centery):
            self.display_surface.blit(sprite.image, sprite.rect.topleft)
        self.bullet_group.draw(self.display_surface)
        self.all_sprites.update(dt)
        self.bullet_group.update(dt)
        for overlay in self.enemies_overlays.values():
            overlay.display()
        self.overlay.display()
