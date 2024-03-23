import pygame
from settings import *


class PlanetPlayer(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.image = pygame.Surface((64, 32))
        self.image.fill('green')
        self.rect = self.image.get_rect(center=pos)
