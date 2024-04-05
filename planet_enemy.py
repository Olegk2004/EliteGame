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
    def __init__(self, target, bullet_group, group,coll_pos, pos=(random.randint(0, SCREEN_HEIGHT), random.randint(0, SCREEN_WIDTH))):
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
        self.coll_pos = coll_pos
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

    def move(self, dt, objects):
        for i in range(len(self.coll_pos)):
            current_x = [col_pos[0] for col_pos in self.coll_pos[i]]  # все иксы осязаемых объектов
            current_y = [col_pos[1] for col_pos in self.coll_pos[i]]  # все игреки
            for i in range(len(current_x)):
                if abs(current_x[i] + 15 - self.pos.x - self.direction.x * self.speed * dt) <= EPS:
                    self.statx = 0
                    break
                else:
                    self.statx = 1

            for i in range(len(current_y)):
                if abs(current_y[i] - self.pos.y - self.direction.y * self.speed * dt) <= EPS:
                    self.staty = 0
                    break
                else:
                    self.staty = 1

            if self.staty + self.statx == 0:
                break

        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        if 20 + self.rect.x // 2 <= self.pos.x + self.direction.x * self.speed * dt <= SCREEN_WIDTH - 20:
            self.statx = self.statx + self.staty
            if self.statx:
                self.pos.x += self.direction.x * self.speed * dt
            else:
                self.pos.x += 0

            self.rect.centerx = self.pos.x

        if 30 <= self.pos.y + self.direction.y * self.speed * dt <= (SCREEN_HEIGHT - 30):
            self.staty = self.staty + self.statx
            if self.staty:
                self.pos.y += self.direction.y * self.speed * dt
            else:
                self.pos.y += 0

            self.rect.centery = self.pos.y

        self.dx = self.target.pos[0] - self.pos[0]
        self.dy = self.target.pos[1] - self.pos[1]
        self.dist = math.hypot(self.dx, self.dy)

        if 30 < self.dist < 300:
            self.direction.x = int(math.copysign(1, self.dx))
            self.direction.y = int(math.copysign(1, self.dy))
        else:
            self.direction = pygame.Vector2()

    def update(self, dt):
        self.update_timers()
        if self.selected_tool == 'gun':
            self.try_shoot()
        self.move(dt, self.coll_pos)
        self.animate(dt)
