import math
import random
import pygame
from settings import *
from timer import Timer


class PlanetEnemy(pygame.sprite.Sprite):
    def __init__(self, target, bullet_group, group, obstacle_sprites,
                 pos=(random.randint(0, SCREEN_HEIGHT), random.randint(0, SCREEN_WIDTH))):
        super().__init__(group)
        self.bullet_group = bullet_group

        self.target = target

        self.hp = 1000

        self.image_status = "idle"
        self.image_frame = 1

        self.direction = pygame.math.Vector2()

        self.obstacle_sprites = obstacle_sprites
        self.image = self.import_image()
        self.rect = self.image.get_rect(center=pos)

        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        self.attack_radius = 300
        self.notice_radius = 500

        # player interaction
        self.can_attack = True

    def import_image(self):
        path = "Images/Enemies/sceleton/" + self.image_status + str(int(self.image_frame) + 1) + ".png"
        now_image = pygame.image.load(path).convert_alpha()
        now_image = pygame.transform.scale(now_image, (64, 64))
        return now_image

    def animate(self, dt):
        self.image_frame += 4 * dt
        print(self.image_frame)
        if self.image_frame >= 5:  # больше 3, потому что количество спрайтов для анимации равно 3
            if self.status == "attack":
                self.can_attack = False
            self.image_frame = 0
        self.image = self.import_image()

    def move(self, dt):
        # Нормализация вектора. Это нужно, чтобы скорость по диагонали была такая же
        if self.direction.magnitude() > 0:  # если мы куда-то двигаемся то нормализуем
            self.direction = self.direction.normalize()

        # перемещение по горизонтали
        self.pos.x += self.direction.x * self.speed * dt  # обновляем позицию игрока в зависимости от направления и скорости
        self.rect.centerx = self.pos.x  # устанавливаем центр спрайта в текущую позицию игрока
        self.collision('horizontal')

        # перемещение по вертикали
        self.pos.y += self.direction.y * self.speed * dt  # обновляем позицию игрока в зависимости от направления и скорости
        self.rect.centery = self.pos.y  # устанавливаем центр спрайта в текущую позицию игрока
        self.collision('vertical')

        if self.direction.y < 0:
            _image_status = "up"
        if self.direction.y > 0:
            _image_status = "down"
        else:
            self.direction.y = 0

        if self.direction.x < 0:
            _image_status = "left"
        elif self.direction.x > 0:
            self.direction.x = 1
            _image_status = "right"
        else:
            self.direction.x = 0

        if self.direction.x == 0 and self.direction.y == 0:  # если остаемся на месте
            _image_status = "idle"

        if not "attack" in self.image_status:
            self.image_status = _image_status

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.width * 0.2)
                sprite_hitbox = sprite.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.width * 0.2)
                if sprite_hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite_hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite_hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                    self.pos.x = self.hitbox.centerx

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.width * 0.2)
                sprite_hitbox = sprite.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.width * 0.2)
                if sprite_hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite_hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite_hitbox.bottom
                    self.rect.centery = self.hitbox.centery
                    self.pos.y = self.hitbox.centery

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            self.status = "attack"
        elif distance <= self.notice_radius:
            self.status = "move"
        else:
            self.status = "idle"

    def actions(self, player):
        if self.status == "attack":
            self.direction = self.get_player_distance_direction(self.target)[1]
        if self.status == "move":
            self.direction = self.get_player_distance_direction(self.target)[1]
        else:
            self.direction = pygame.math.Vector2()

    def update(self, dt):
        self.get_status(self.target)
        self.actions(self.target)
        print(self.direction)
        self.move(dt)
        self.animate(dt)
