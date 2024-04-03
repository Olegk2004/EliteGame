import pygame
import galaxy
import math
import system_generator
import plansys
from debug import debug
from math import sqrt
from settings import *


class Planet(pygame.sprite.Sprite):
    def __init__(self, image, pos, radius, group):
        super().__init__(group)
        self.pos = pos
        self.radius = radius
        self.image = image
        self.image = pygame.transform.scale(self.image, (self.radius * 10, self.radius * 10))
        self.rect = self.image.get_rect(center=self.pos)


class CameraGroup(pygame.sprite.Group):
    def __init__(self, surface, galaxy, player):
        super().__init__()
        self.display_surface = surface
        self.galaxy = galaxy
        self.player = player

        for system in self.galaxy.systems:
            if system == self.player.current_planet:  # если это текущая планета игрока, то рисуем одним цветом
                system.sprite = Planet(CURRENT_PLANET_IMAGE.convert_alpha(), (system.x, system.y), 5, self)
            elif system in self.player.visited_planets:  # если это посещенная планета, то другим
                system.sprite = Planet(STANDART_PLANET_IMAGE.convert_alpha(), (system.x, system.y), 3, self)
            else:
                if system.gold_planet != 0:
                    system.sprite = Planet(SUPER_FUEL_PLANET_IMAGE.convert_alpha(), (system.x, system.y), 4, self)
                elif system.fuel_station_value != 0:
                    system.sprite = Planet(FUEL_STATION_PLANET_IMAGE.convert_alpha(), (system.x, system.y), 3, self)
                else:
                    system.sprite = Planet(STANDART_PLANET_IMAGE.convert_alpha(), (system.x, system.y), 3, self)

        # camera offset
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # box setup
        self.camera_borders = {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.display_surface.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.display_surface.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l, t, w, h)

        background_image = pygame.image.load('Images/galaxy_map_square_background.png').convert_alpha()
        self.background_surf = pygame.transform.scale(background_image, (MAP_WIDTH, MAP_HEIGHT))
        self.background_rect = self.background_surf.get_rect(topleft=(0, 0))

        # camera speed
        self.keyboard_speed = 20
        self.mouse_speed = 0.2

        # zoom
        self.zoom_scale = 1
        self.internal_surf_size = (MAP_WIDTH, MAP_HEIGHT)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center=(self.half_w, self.half_h))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h

        self.scaled_surf = None
        self.scaled_rect = None

    def center_target_camera(self, target):
        self.offset = pygame.math.Vector2(self.player.current_planet.sprite.rect.centerx - self.half_w,
                                          self.player.current_planet.sprite.rect.centery - self.half_h)

    def keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.camera_rect.x -= self.keyboard_speed
        if keys[pygame.K_RIGHT]:
            self.camera_rect.x += self.keyboard_speed
        if keys[pygame.K_UP]:
            self.camera_rect.y -= self.keyboard_speed
        if keys[pygame.K_DOWN]:
            self.camera_rect.y += self.keyboard_speed

        self.offset.x += self.camera_rect.left - self.camera_borders['left']
        self.offset.y += self.camera_rect.top - self.camera_borders['top']

    def zoom_keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_EQUALS] and self.zoom_scale - 2 < 0.05:
            self.zoom_scale += 0.05
        if keys[pygame.K_MINUS] and self.zoom_scale - 0.20 > 0.05:
            self.zoom_scale -= 0.05

    def draw(self):
        self.center_target_camera(self.player.current_planet)
        self.keyboard_control()
        self.zoom_keyboard_control()

        self.internal_surf.fill('black')
        background_offset = self.background_rect.topleft - self.offset + self.internal_offset
        self.internal_surf.blit(self.background_surf, background_offset)

        self.player.current_planet.sprite.kill()
        self.player.current_planet.sprite = Planet(CURRENT_PLANET_IMAGE, (self.player.current_planet.x, self.player.current_planet.y), 5, self)
        for match in self.galaxy.matches[self.player.current_planet]:
            if match in self.player.visited_planets:
                match.sprite.kill()
                match.sprite = Planet(STANDART_PLANET_IMAGE, (match.x, match.y), 3, self)
            pygame.draw.line(self.internal_surf, EDGES_COLOR, self.player.current_planet.sprite.rect.center - self.offset + self.internal_offset,
                             match.sprite.rect.center - self.offset + self.internal_offset, 2)
        # active elements
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
            self.internal_surf.blit(sprite.image, offset_pos)

        self.scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surface_size_vector * self.zoom_scale)
        self.scaled_rect = self.scaled_surf.get_rect(center=(self.half_w, self.half_h))

        self.display_surface.blit(self.scaled_surf, self.scaled_rect)


class Map:
    def __init__(self, galaxy, player):
        self.galaxy = galaxy
        self.player = player
        self.all_sprites = pygame.sprite.Group()
        self.map_screen = pygame.surface.Surface((MAP_PANEL_WIDTH, MAP_PANEL_HEIGHT))
        self.camera_group = CameraGroup(self.map_screen, self.galaxy, self.player)
        self.border = pygame.surface.Surface((SCREEN_WIDTH - MAP_PANEL_WIDTH, SCREEN_HEIGHT))  # Для работы с областью справа
        self.rect = self.map_screen.get_rect()

        '''
        MINIMAP_WIDTH = SCREEN_WIDTH - MAP_PANEL_WIDTH
        MINIMAP_HEIGHT = SCREEN_HEIGHT - MAP_PANEL_HEIGHT
        self.minimap_surface = pygame.surface.Surface((MINIMAP_WIDTH, MINIMAP_HEIGHT))
        self.minimap_rect = self.minimap_surface.get_rect(topleft=(SCREEN_WIDTH - MINIMAP_WIDTH, 0))
        self.minimap_scale = 0.1
        '''

    def distance_to(self, destination_planet):
        return int(4 * sqrt(
            (self.player.current_planet.x - destination_planet.x) * (
                        self.player.current_planet.x - destination_planet.x) + (
                        self.player.current_planet.y - destination_planet.y) * (
                    self.player.current_planet.y - destination_planet.y) / 4))

    def draw(self):
        self.camera_group.update()
        self.camera_group.draw()

    def draw_side_panel(self, surface, fuel, ration, checked_mouse):
        LEN_CONST = 200 / FUEL_CONST
        len_of_bar = fuel * LEN_CONST  # Нормировка длины полоски

        if self.player.fuel > self.player.fuel_const:
            const_len_of_bar = self.player.fuel * LEN_CONST  # Расширяет основную шкалу топлива, если топливо стало больше, чем было изначально(можно, конено, ограничить всё нововедённой переменной)
            des_of_bar_save = self.player.fuel * LEN_CONST
            self.player.fuel_const = self.player.fuel

        else:
            const_len_of_bar = self.player.fuel_const * LEN_CONST  # Постоянная длина синих границ полоски
            des_of_bar_save = self.player.bar_save * LEN_CONST  # Для сохранения координаты, до куда в прошлый раз коцнулась полоска
        len_of_got_bar = 0
        len_of_spent_bar = (des_of_bar_save - len_of_bar)  # Длина коцки
        if len_of_spent_bar < 0:
            len_of_spent_bar = 0
            len_of_got_bar = len_of_bar - des_of_bar_save

        pygame.draw.rect(self.map_screen, (255, 255, 255), self.rect, 2)
        self.border.fill((0, 0, 0))
        '''
        # Draw the minimap
        self.border.fill((0, 0, 0))
        for system in self.galaxy.systems:
            # Calculate the position of the system on the minimap
            system_pos = (int(system.x * self.minimap_scale), int(system.y * self.minimap_scale))
            pygame.draw.circle(self.minimap_surface, (255, 255, 255), system_pos, 2)  # Draw a small dot for each system

        # Draw the sliding window on the minimap
        sliding_window_rect = pygame.Rect(
            self.camera_group.offset[0] * self.minimap_scale,
            self.camera_group.offset[1] * self.minimap_scale,
            self.rect.width * self.minimap_scale / self.camera_group.zoom_scale,
            self.rect.height * self.minimap_scale / self.camera_group.zoom_scale
        )
        pygame.draw.rect(self.minimap_surface, (0, 255, 0), sliding_window_rect, 2)
        '''
        pygame.draw.rect(self.border, (255, 255, 255), (-2, 448, 304, 750), 2)  # границы полей справа, область снизу
        pygame.draw.rect(self.border, (255, 255, 255), (0, 350, 300, 5), 5)  # область по середине
        pygame.draw.rect(self.border, (255, 255, 255), (0, 0, 300, 2), 5)  # верхняя область

        pygame.draw.rect(self.border, (0, 0, 255), (3, 315, const_len_of_bar, 35), 5)  # Параметры полоски топлива
        pygame.draw.rect(self.border, (255, 0, 0), (6, 320, const_len_of_bar - 7, 25), 13)
        pygame.draw.rect(self.border, (0, 255, 0), (6, 320, len_of_bar - 7, 25), 13)

        pygame.font.init()  # инициализация текста
        my_font = pygame.font.SysFont('Comic Sans MS', 15)  # его параметры
        text_surface = my_font.render(f'У вас топлива: {self.player.fuel}, max: {MAX_FUEL_VALUE}', False,
                                      (255, 255, 255))
        text2 = my_font.render(f'Вы находитесь на планете: ', False, (255, 255, 255))
        text3 = my_font.render(f'{self.player.current_planet.name}', False, (255, 255, 255))
        text4 = my_font.render(f'Тип планеты: ', False, (255, 255, 255))
        text5 = my_font.render(f'{self.player.current_planet.type}', False, (255, 255, 255))
        text6 = my_font.render(f'Ресурсы: ', False, (255, 255, 255))
        text7 = my_font.render(f'Топливо: ', False, (255, 255, 255))
        text12 = my_font.render(f"", False, (0, 0, 0))
        text9 = my_font.render("", False, (255, 255, 255))
        text8 = my_font.render(f'{self.player.current_planet.fuel_station_value_save}', False, (255, 255, 255))
        text13 = text10 = text11 = my_font.render(f"", False, (0, 0, 0))
        text15 = my_font.render(f"Кол-во посещённых планет: {len(self.player.visited_planets)}", False, (255, 255, 255))
        if checked_mouse in self.player.visited_planets:
            text9 = my_font.render(f'Планета : {checked_mouse.name}', False,
                                   (255, 255, 255))  # Пошла информация о наведённой курсором планете
            # text10 = my_font.render(f'Доступные ресурсы: ', False, (255, 255, 255))
            # text11 = my_font.render(f'Топливо: {checked_mouse.fuel_station_value}', False, (255, 255, 255))
            text12 = my_font.render(f'Необходимо топлива: {self.distance_to(checked_mouse)}', False, (255, 255, 255))

        elif checked_mouse in self.galaxy.matches[self.player.current_planet]:
            text13 = my_font.render(f'Неисследованная планета', False, (255, 255, 255))
            text12 = my_font.render(f'Необходимо топлива: {self.distance_to(checked_mouse)}', False, (255, 255, 255))
        elif checked_mouse in self.galaxy.systems:
            text13 = my_font.render(f'Неисследованная планета', False, (255, 255, 255))
            text12 = my_font.render('Необходимо топлива: неизвестно', False, (255, 255, 255))
        else:
            text9 = my_font.render("Космическое пространство", False, (255, 255, 255))
            text12 = text13 = text10 = text11 = my_font.render(f"", False, (0, 0, 0))

        pygame.draw.rect(self.border, (255, 255, 0),
                         (des_of_bar_save - len_of_spent_bar - 1, 320, len_of_spent_bar * int(ration) / 100, 25),
                         13)  # Анимированный расход топлива
        pygame.draw.rect(self.border, (255, 0, 255), (
        des_of_bar_save + len_of_got_bar * int(-ration) / 100 + len_of_got_bar, 320, len_of_got_bar * int(ration) / 100,
        25), 14)

        surface.blit(self.map_screen, self.rect)
        self.border.blit(text_surface, (40, 5))  # У вас топлива
        self.border.blit(text2, (40, 25))  # Вы находитесь
        self.border.blit(text3, (40, 40))
        self.border.blit(text4, (40, 65))  # Тип планеты
        self.border.blit(text5, (40, 80))
        self.border.blit(text6, (40, 105))  # Ресурсы
        self.border.blit(text7, (40, 120))
        self.border.blit(text15, (40, 140))
        self.border.blit(text8, (115, 120))
        self.border.blit(text9, (5, 375))
        self.border.blit(text10, (5, 395))
        self.border.blit(text11, (5, 415))
        self.border.blit(text12, (5, 415))
        self.border.blit(text13, (5, 395))

        '''
        # Blit the minimap onto the side panel
        self.minimap_surface.fill((255, 0, 0))
        self.border.blit(self.minimap_surface, self.minimap_rect.topleft)
        '''
        surface.blit(self.border, (SCREEN_HEIGHT, 0))

    def check_click(self, click_pos):
        for planet in self.galaxy.matches[self.player.current_planet]:
            # Calculate the offset of the planet sprite relative to the visible area
            offset_sprite_cords = planet.sprite.rect.center - self.camera_group.offset + self.camera_group.internal_offset

            # Adjust the offset
            adjusted_offset_sprite_cords = (
                offset_sprite_cords[0] + self.camera_group.scaled_rect.left,
                offset_sprite_cords[1] + self.camera_group.scaled_rect.top
            )

            # Calculate the zoomed coordinates of the planet sprite within the visible area
            zoomed_sprite_cords = (
                (adjusted_offset_sprite_cords[0]), # * self.camera_group.zoom_scale),
                (adjusted_offset_sprite_cords[1]) # * self.camera_group.zoom_scale)
            )

            # Calculate the distance between the click position and the zoomed sprite coordinates
            distance = ((zoomed_sprite_cords[0] - click_pos[0]) ** 2 +
                        (zoomed_sprite_cords[1] - click_pos[1]) ** 2) ** 0.5

            # Calculate the radius of the planet based on its sprite size
            planet_radius = (((planet.sprite.rect.topleft[0] - planet.sprite.rect.center[0]) * self.camera_group.zoom_scale) ** 2 +
                             ((planet.sprite.rect.topleft[1] - planet.sprite.rect.center[1]) * self.camera_group.zoom_scale) ** 2) ** 0.5
            # Check if the distance is within the planet radius scaled by the zoom factor
            if distance < planet_radius:
                return planet
        return None

    def check_mouse(self, mouse_pos):
        for planet in self.galaxy.systems:
            # Calculate the offset of the planet sprite relative to the visible area
            offset_sprite_cords = planet.sprite.rect.center - self.camera_group.offset + self.camera_group.internal_offset

            # Adjust the offset
            adjusted_offset_sprite_cords = (
                offset_sprite_cords[0] + self.camera_group.scaled_rect.left,
                offset_sprite_cords[1] + self.camera_group.scaled_rect.top
            )

            # Calculate the zoomed coordinates of the planet sprite within the visible area
            zoomed_sprite_cords = (
                (adjusted_offset_sprite_cords[0]),  # * self.camera_group.zoom_scale),
                (adjusted_offset_sprite_cords[1])  # * self.camera_group.zoom_scale)
            )

            # Calculate the distance between the click position and the zoomed sprite coordinates
            distance = ((zoomed_sprite_cords[0] - mouse_pos[0]) ** 2 +
                        (zoomed_sprite_cords[1] - mouse_pos[1]) ** 2) ** 0.5

            # Calculate the radius of the planet based on its sprite size
            planet_radius = (((planet.sprite.rect.topleft[0] - planet.sprite.rect.center[
                0]) * self.camera_group.zoom_scale) ** 2 +
                             ((planet.sprite.rect.topleft[1] - planet.sprite.rect.center[
                                 1]) * self.camera_group.zoom_scale) ** 2) ** 0.5
            # Check if the distance is within the planet radius scaled by the zoom factor
            if distance < planet_radius:
                return planet
        return None