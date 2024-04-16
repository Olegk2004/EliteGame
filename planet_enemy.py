from math import sin
import random
import pygame
from settings import *
from timer import Timer


class PlanetEnemy(pygame.sprite.Sprite):
    def __init__(self, target, group, obstacle_sprites, damage_player,
                 pos=(random.randint(0, SCREEN_HEIGHT), random.randint(0, SCREEN_WIDTH))):
        super().__init__(group)

        self.target = target

        self.hp = 300

        self.image_status = "idle"
        self.image_frame = 1

        self.direction = pygame.math.Vector2()

        self.obstacle_sprites = obstacle_sprites
        self.image = self.import_image()
        self.rect = self.image.get_rect(center=pos)

        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 100

        self.attack_radius = 20
        self.notice_radius = 500

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player

        # invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invinsibility_duration = 300

    def import_image(self):
        path = "Images/Enemies/sceleton/" + self.image_status + str(int(self.image_frame) + 1) + ".png"
        now_image = pygame.image.load(path).convert_alpha()
        now_image = pygame.transform.scale(now_image, (64, 64))
        return now_image

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invinsibility_duration:
                self.vulnerable = True

    def get_damage(self, player):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            self.hp -= 100
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.hp <= 0:
            self.kill()

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -3

    def animate(self, dt):
        self.image_frame += 4 * dt
        if self.image_frame >= 5:  # больше 3, потому что количество спрайтов для анимации равно 3
            if self.status == "atack":
                self.can_attack = False
            self.image_frame = 0

        if not self.vulnerable:  # если враг атакован
            opposite = {"up": "down", "down": "up", "left": "right", "right": "left", "idle": "idle"}
            self.image_status = opposite[self.image_status]

        self.image = self.import_image()
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

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

        if distance <= self.attack_radius:
            self.status = "attack"
        elif distance <= self.notice_radius:
            self.status = "move"
        else:
            self.status = "idle"

    def actions(self, player):
        if self.status == "attack":
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(100)
            # self.direction = self.get_player_distance_direction(self.target)[1]
        if self.status == "move":
            self.direction = self.get_player_distance_direction(self.target)[1]
        else:
            self.direction = pygame.math.Vector2()

    def update(self, dt):
        self.get_status(self.target)
        self.actions(self.target)
        self.hit_reaction()
        self.move(dt)
        self.animate(dt)
        self.cooldowns()
        self.check_death()
