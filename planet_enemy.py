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
        self.speed = 350

    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos
        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
            self.kill()  # Убиваем пулю, если она выходит за пределы экрана


class PlanetEnemy(pygame.sprite.Sprite):
    def __init__(self, target, bullet_group, group, pos=(random.randint(0, SCREEN_HEIGHT), random.randint(0, SCREEN_WIDTH))):
        super().__init__(group)
        self.bullet_group = bullet_group

        self.target = target

        self.image_status = "idle"
        self.image_frame = 1

        colors = {0: 'red', 1: 'orange', 2: 'yellow', 3: 'green', 4: 'blue', 5: 'purple'}  # Пока нет норм спрайтов, сделал различимые градиенты
        start_color_id = random.choice(range(len(colors)))
        self.start_color = pygame.Color(colors[start_color_id])
        self.end_color = pygame.Color(colors[(start_color_id + 1) % len(colors)])
        self.gradient_tick = 0
        self.gradient_speed = 0.01

        self.direction = pygame.math.Vector2()

        # Таймеры
        self.timers = {
            'shot': Timer(500),
            'fire delay': Timer(50),
            'reload': Timer(1000)
        }

        self.image = self.import_image()
        self.rect = self.image.get_rect(center=pos)

        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = random.randint(100, 200)

        # Расстояние до цели
        self.dx = self.target.pos[0] - self.pos[0]
        self.dy = self.target.pos[1] - self.pos[1]
        self.dist = math.hypot(self.dx, self.dy)

        # Оружие
        self.tools = ['sword', 'gun']
        self.tool_index = random.randint(0, len(self.tools) - 1)
        self.selected_tool = self.tools[self.tool_index]

    def import_image(self):
        now_image = pygame.Surface((40, 60))
        if self.timers['shot'].active:
            color = pygame.Color('white')
        else:
            color = pygame.Color(int(self.start_color.r + (self.end_color.r - self.start_color.r) * self.gradient_tick),
                                 int(self.start_color.g + (self.end_color.g - self.start_color.g) * self.gradient_tick),
                                 int(self.start_color.b + (self.end_color.b - self.start_color.b) * self.gradient_tick))
            if self.direction != (0, 0):
                self.gradient_tick += self.gradient_speed
            if self.gradient_tick > 1:
                self.gradient_tick = 0
        now_image.fill(color)
        return now_image

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def try_shoot(self):
        if not self.timers['shot'].active:
            if self.selected_tool == 'gun' and self.dist < 500:
                shot_prob = 0.1
                if random.random() < shot_prob:
                    self.shoot()

    def shoot(self):
        if not self.timers['reload'].active:
            self.timers['shot'].activate()
            shot_series = [1, 3, 5]
            number_of_shots = random.choices(shot_series, [0.8, 0.15, 0.05])[0]
            for _ in range(number_of_shots):
                bullet = Bullet(self.pos, (self.dx, self.dy), self.bullet_group)
                self.timers['fire delay'].activate()
            self.timers['reload'].activate()


    def animate(self, dt):
        self.image_frame += 4 * dt
        if self.image_frame >= 4:  # больше 3, потому что количество спрайтов для анимации равно 3
            self.image_frame = 0
        self.image = self.import_image()

    def move(self, dt):
        if not self.timers['shot'].active:

            if 30 < self.dist < 300:
                self.direction.x = int(math.copysign(1, self.dx))  # -1 если враг справа от игрока, 1 если слева
                self.direction.y = int(math.copysign(1, self.dy))  # -1 если враг снизу от игрока, 1 если сверху
            else:
                self.direction = pygame.Vector2()

            if self.direction.magnitude() > 0:  # если мы куда-то двигаемся то нормализуем
                self.direction = self.direction.normalize()
            # перемещение по горизонтали
            if 20 + self.rect.x // 2 <= self.pos.x + self.direction.x * self.speed * dt <= SCREEN_WIDTH - 20:
                self.pos.x += self.direction.x * self.speed * dt
                #self.pos.x += random.randint(0, self.speed) * dt
                self.rect.centerx = self.pos.x  # устанавливаем центр спрайта в текущую позицию врага
            # перемещение по вертикали
            if 30 <= self.pos.y + self.direction.y * self.speed * dt <= (SCREEN_HEIGHT - 30):
                self.pos.y += self.direction.y * self.speed * dt
                #self.pos.y += random.randint(0, self.speed) * dt
                self.rect.centery = self.pos.y  # устанавливаем центр спрайта в текущую позицию врага
            self.dx = self.target.pos[0] - self.pos[0]
            self.dy = self.target.pos[1] - self.pos[1]
            self.dist = math.hypot(self.dx, self.dy)

    def update(self, dt):
        self.update_timers()
        if self.selected_tool == 'gun':
            self.try_shoot()
        self.move(dt)
        self.animate(dt)
