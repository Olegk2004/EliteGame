import pygame
from settings import *


class PlanetPlayer(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.image = pygame.Surface((8, 8))
        self.image.fill('green')
        self.rect = self.image.get_rect(center=pos)

        # movement attributes
        self.direction = pygame.math.Vector2()  # направление, определяется вектором. Во время обновления координаты игрока меняются в зависимости от направления
        self.pos = pygame.math.Vector2(self.rect.center)  # координаты игрока
        self.speed = 200

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self, dt):
        # Нормализация ветора. Это нужно, чтобы скорость по диагонали была такая же
        if self.direction.magnitude() > 0: # если мы куда-то двигаемся то нормализуем
            self.direction = self.direction.normalize()

        # перемещение по горизонтали
        self.pos.x += self.direction.x * self.speed * dt  # обновляем позицию игрока в зависимости от направления и скорости
        self.rect.centerx = self.pos.x  # устанавливаем центр спрайта в текущую позицию игрока

        # перемещение по вертикали
        self.pos.y += self.direction.y * self.speed * dt  # обновляем позицию игрока в зависимости от направления и скорости
        self.rect.centery = self.pos.y  # устанавливаем центр спрайта в текущую позицию игрока

    def update(self, dt):
        self.input()
        self.move(dt)

