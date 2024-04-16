import pygame
from settings import *


class Magic(pygame.sprite.Sprite):
    def __init__(self, direction, pos, group, obstacle_sprites):
        super().__init__(group)
        # stats
        self.attack_amount = 100

        # image
        self.image_frame = 0
        self.image = self.import_image()
        self.rect = self.image.get_rect(center=pos)

        # movement
        self.direction = direction

        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        self.obstacle_sprites = obstacle_sprites


    def import_image(self):
        path = "Images/tools/magic/" + str(int(self.image_frame) + 1) + ".png"
        now_image = pygame.image.load(path).convert_alpha()
        now_image = pygame.transform.scale(now_image, (16, 16))
        return now_image

    def move(self, dt):
        if self.direction.magnitude() > 0:  # если мы куда-то двигаемся то нормализуем
            self.direction = self.direction.normalize()
        self.pos.x += self.direction.x * self.speed * dt  # обновляем позицию игрока в зависимости от направления и скорости
        self.rect.centerx = self.pos.x  # устанавливаем центр спрайта в текущую позицию игрока

        # перемещение по вертикали
        self.pos.y += self.direction.y * self.speed * dt  # обновляем позицию игрока в зависимости от направления и скорости
        self.rect.centery = self.pos.y  # устанавливаем центр спрайта в текущую позицию игрока

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.rect.colliderect(self.rect):
                    self.kill()

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.width * 0.2)
                sprite_hitbox = sprite.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.width * 0.2)
                if sprite_hitbox.colliderect(self.hitbox):
                    self.kill()

    def animate(self, dt):
        self.image_frame += 12 * dt
        if self.image_frame >= 30:
            self.kill()
        else:
            self.image = self.import_image()

    def update(self, dt):
        self.move(dt)
        self.animate(dt)
