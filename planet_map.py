import pygame
import galaxy
import math
import system_generator
from settings import *
from debug import debug
from planet_player import PlanetPlayer
from planet_enemy import PlanetEnemy
from overlay import Overlay
from pytmx.util_pygame import load_pygame


# pip install pytmx

class Collisions(pygame.sprite.Sprite):  # пока не использую, мало ли пригодиться( класс осязаемых объектов)
    def __init__(self, pos, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)

        # movement attributes
        self.direction = pygame.math.Vector2()  # направление, определяется вектором. Во время обновления координаты игрока меняются в зависимости от направления
        self.pos = pygame.math.Vector2(self.rect.center)


class Tile(pygame.sprite.Sprite):  # пока не использую, класс тайл-карт
    def __init__(self, pos, surf):
        super().__init__()
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)


class PlanetMap:
    def __init__(self, planet):
        self.planet = planet
        self.all_sprites = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.display_surface = pygame.display.get_surface()
        self.stat = 0  # флаг на одноразовый вызов метоа сэтап (там мы передаём позиции в планет_мап)
        self.stat2 = 1  # флаг на одноразовое заполнение массива позиций
        self.switch = 0
        self.coll = []  # массив позиций
        self.colls = []
        # self.setup()

    def setup(self, coll_pos):
        self.planet_player = PlanetPlayer((50, 350), self.all_sprites,
                                          coll_pos)  # теперь в аргументах указываем ещё и позиции осязаемых объектов

        self.planet_enemies = {}
        self.enemies_overlays = {}
        # for i in range(NUM_OF_ENEMIES): # в сеттингс добавил кол-во врагов, пока закомментил
        # self.planet_enemies['enemy_' + str(i)] = PlanetEnemy(self.planet_player, self.bullet_group,
        # self.all_sprites, (500, 100 + i * 100))
        # self.enemies_overlays['enemy_' + str(i)] = Overlay(self.display_surface,
        # self.planet_enemies['enemy_' + str(i)])

        self.overlay = Overlay(self.display_surface, self.planet_player)

    def draw(self, dt):
        self.display_surface.fill('black')
        tmx_data = load_pygame("Tiles/tile2.tmx")  # берём тайл-карту

        for layer in tmx_data.visible_layers:  # по всем видимым уровням тайл-карты

            if hasattr(layer, 'data'):  # необязательно
                for x, y, surf in layer.tiles():  # каждый икс и игрек и поверхность(рисуночек тайла отдельного) текущего уровня
                    pos = (x * 32, y * 32)  # tile выравниваем каждый тайл
                    tile = Tile(pos=pos, surf=surf)  # пока не надо
                    if layer.name == "second" and self.stat2 != 0:  # если это тайл второго уровня(гле осязаемые объекты) и при этом мы добавляли его позиции ниразу, то
                        if len(self.coll) == 0:
                            self.coll.append([x * 32, y * 32])  # добавляем позиции осязаемого объекта
                            continue
                        current_x = [col_pos[0] for col_pos in self.coll]  # все иксы осязаемых объектов
                        current_y = [col_pos[1] for col_pos in self.coll]  # все игреки
                        new_x = [abs(xx - x * 32) for xx in current_x]
                        new_y = [abs(yy - y * 32) for yy in current_y]
                        if min(new_x) <= 32 and min(new_y) == 0 or min(new_y) <= 32 and min(new_x) == 0 :
                            self.coll.append([x * 32, y * 32])  # добавляем позиции осязаемого объекта
                        else:
                            self.colls.append(self.coll)
                            self.coll = []
                            self.coll.append([x * 32, y * 32])
                        print(len(self.coll), self.coll, self.colls)

                    self.display_surface.blit(surf, pos)  # блитуем
        if self.switch == 0:
            self.colls.append(self.coll)
            self.switch = 1
            print("here - ", self.colls)

        for sprite in sorted(self.all_sprites, key=lambda sprite: sprite.rect.centery):
            self.display_surface.blit(sprite.image, sprite.rect.topleft)

        self.bullet_group.draw(self.display_surface)
        self.all_sprites.update(dt)
        self.bullet_group.update(dt)
        # for overlay in self.enemies_overlays.values():
        # overlay.display()
        if self.stat == 0:  # меняем необходимые флаги
            self.setup(self.colls)  # передаём позиции осязаемых позиций
            self.stat = 1
            self.stat2 = 0

        self.overlay.display()
