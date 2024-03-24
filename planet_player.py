import pygame
from settings import *


class PlanetPlayer(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.image_status = "idle"  # для определения какого направления спрайт вставлять
        self.image_frame = 1  # для реализации анимации
        # для анимации нужны несколько картинок в одном направлении, чтобы они менялись каждые несколько милисекунд

        self.image = self.import_image()
        self.rect = self.image.get_rect(center=pos)

        # movement attributes
        self.direction = pygame.math.Vector2()  # направление, определяется вектором. Во время обновления координаты игрока меняются в зависимости от направления
        self.pos = pygame.math.Vector2(self.rect.center)  # координаты игрока
        self.speed = 200

    def import_image(self):
        path = "Images/player_" + self.image_status + "_" + str(int(self.image_frame) + 1) + ".png"
        now_image = pygame.image.load(path)
        now_image = pygame.transform.scale(now_image, (40, 60))
        return now_image

    def animate(self, dt):
        self.image_frame += 4 * dt
        if self.image_frame >= 4:  # больше 3, потому что количество спрайтов для анимации равно 3
            self.image_frame = 0
        self.image = self.import_image()

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.image_status = "up"
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.image_status = "down"
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.image_status = "left"
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.image_status = "right"
        else:
            self.direction.x = 0

        if self.direction.x == 0 and self.direction.y == 0:  # если остаемся на месте
            self.image_status = "idle"

    def move(self, dt):
        # Нормализация ветора. Это нужно, чтобы скорость по диагонали была такая же
        if self.direction.magnitude() > 0:  # если мы куда-то двигаемся то нормализуем
            self.direction = self.direction.normalize()

        # перемещение по горизонтали
        if 20 + self.rect.x // 2 <= self.pos.x + self.direction.x * self.speed * dt <= SCREEN_WIDTH - 20:
            self.pos.x += self.direction.x * self.speed * dt  # обновляем позицию игрока в зависимости от направления и скорости
            self.rect.centerx = self.pos.x  # устанавливаем центр спрайта в текущую позицию игрока

        # перемещение по вертикали
        if 30 <= self.pos.y + self.direction.y * self.speed * dt <= (SCREEN_HEIGHT - 30):
            self.pos.y += self.direction.y * self.speed * dt  # обновляем позицию игрока в зависимости от направления и скорости
            self.rect.centery = self.pos.y  # устанавливаем центр спрайта в текущую позицию игрока

    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)
        print(self.image_frame)
