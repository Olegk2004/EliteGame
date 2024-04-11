import math
import random
import pygame
from settings import *
from timer import Timer


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, direction, group):
        super().__init__(group)
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.direction = pygame.math.Vector2(direction).normalize()
        self.speed = 100

    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos
        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
            self.kill()  # Убиваем пулю, если она выходит за пределы экрана


class PlanetEnemy(pygame.sprite.Sprite):
    def __init__(self, target, bullet_group, group, coll_pos,
                 pos=(random.randint(0, SCREEN_HEIGHT), random.randint(0, SCREEN_WIDTH))):
        super().__init__(group)
        self.bullet_group = bullet_group

        self.target = target

        self.image_status = "idle"
        self.image_frame = 1

        colors = {0: 'red', 1: 'orange', 2: 'yellow', 3: 'green', 4: 'blue',
                  5: 'purple'}  # Пока нет норм спрайтов, сделал различимые градиенты
        start_color_id = random.choice(range(len(colors)))
        self.start_color = pygame.Color(colors[start_color_id])
        self.end_color = pygame.Color(colors[(start_color_id + 1) % len(colors)])
        self.gradient_tick = 0
        self.gradient_speed = 0.01

        self.direction = pygame.math.Vector2()

        self.obstacle_sprites = coll_pos
        self.image = self.import_image()
        self.rect = self.image.get_rect(center=pos)

        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        self.attack_radius = 300
        self.notice_radius = 500


    def import_image(self):
        now_image = pygame.Surface((40, 60))
        color = pygame.Color(int(self.start_color.r + (self.end_color.r - self.start_color.r) * self.gradient_tick),
                            int(self.start_color.g + (self.end_color.g - self.start_color.g) * self.gradient_tick),
                            int(self.start_color.b + (self.end_color.b - self.start_color.b) * self.gradient_tick))
        if self.direction != (0, 0):
            self.gradient_tick += self.gradient_speed
        if self.gradient_tick > 1:
            self.gradient_tick = 0
        now_image.fill(color)
        return now_image

    def animate(self, dt):
        self.image_frame += 4 * dt
        if self.image_frame >= 4:  # больше 3, потому что количество спрайтов для анимации равно 3
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

        if distance <= self.attack_radius:
            self.status = "attack"
        elif distance <= self.notice_radius:
            self.status = "move"
        else:
            self.status = "idle"

    def actions(self, player):
        if self.status == "attack":
            self.direction = self.get_player_distance_direction(self.target)[1]
        elif self.status == "move":
            self.direction = self.get_player_distance_direction(self.target)[1]
        else:
            self.direction = pygame.math.Vector2()

    def update(self, dt):
        self.get_status(self.target)
        self.actions(self.target)
        print(self.direction)
        self.move(dt)
        #self.animate(dt)
