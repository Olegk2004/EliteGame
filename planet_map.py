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


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Camera:
    def __init__(self, width, height):
        self.rect = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.rect.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)
        self.rect = pygame.Rect(x, y, self.width, self.height)


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
        self.camera = Camera(self.display_surface.get_width(), self.display_surface.get_height())
        # self.setup()

    def setup(self, coll_pos):
        self.planet_player = PlanetPlayer((50, 350), self.all_sprites,
                                          coll_pos)  # теперь в аргументах указываем ещё и позиции осязаемых объектов

        self.planet_enemies = {}
        self.enemies_overlays = {}
        for i in range(NUM_OF_ENEMIES): # в сеттингс добавил кол-во врагов, пока закомментил
            self.planet_enemies['enemy_' + str(i)] = PlanetEnemy(self.planet_player, self.bullet_group,
                                                                 self.all_sprites,  coll_pos, (500, 100 + i * 100))

        self.overlay = Overlay(self.display_surface, self.planet_player)

    def draw(self, dt):
        self.display_surface.fill('black')
        tmx_data = load_pygame("Tiles/tile2.tmx")  # берём тайл-карту

        for layer in tmx_data.visible_layers:  # по всем видимым уровням тайл-карты

            if hasattr(layer, 'data'):  # необязательно
                for x, y, surf in layer.tiles():  # каждый икс и игрек и поверхность(рисуночек тайла отдельного) текущего уровня
                    pos = (x * TILE_SIZE, y * TILE_SIZE)  # tile выравниваем каждый тайл

                    if layer.name == "second" and self.stat2 != 0:  # если это тайл второго уровня(гле осязаемые объекты) и при этом мы добавляли его позиции ниразу, то
                        if len(self.coll) == 0:
                            self.coll.append([x * TILE_SIZE, y * 32, TILE_SIZE])  # добавляем позиции осязаемого объекта
                            continue
                        current_x = [col_pos[0] for col_pos in self.coll]  # все иксы осязаемых объектов
                        current_y = [col_pos[1] for col_pos in self.coll]  # все игреки
                        new_x = [abs(xx - x * TILE_SIZE) for xx in current_x]
                        new_y = [abs(yy - y * TILE_SIZE) for yy in current_y]
                        if min(new_x) <= 32 and min(new_y) == 0 or min(new_y) <= 32 and min(new_x) == 0 :
                            self.coll.append([x * TILE_SIZE, y * TILE_SIZE, surf])  # добавляем позиции осязаемого объекта
                        else:
                            self.colls.append(self.coll)
                            self.coll = []
                            self.coll.append([x * TILE_SIZE, y * TILE_SIZE, surf])

                    tile = Tile(surf, pos[0], pos[1])
                    self.display_surface.blit(tile.image, self.camera.apply(tile))
        # блитуем
        if self.switch == 0:
            self.colls.append(self.coll)
            self.switch = 1

        for sprite in sorted(self.all_sprites, key=lambda sprite: sprite.rect.centery):
            self.display_surface.blit(sprite.image, self.camera.apply(sprite))

        for bullet in self.bullet_group:
            self.display_surface.blit(bullet.image, self.camera.apply(bullet))
        self.all_sprites.update(dt)
        self.bullet_group.update(dt)

        if self.stat == 0:  # меняем необходимые флаги
            self.setup(self.colls)  # передаём позиции осязаемых позиций
            self.stat = 1
            self.stat2 = 0
        #for overlay in self.enemies_overlays.values():
            #overlay.display()
        self.overlay.display()
        self.camera.update(self.planet_player)
