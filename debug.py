# Этот модуль нужен чтобы выводить всякую инфу для дебаггинга
# в левый верхний угол экрана при запуске игры

import pygame

pygame.init()
font = pygame.font.Font(None, 30)


def debug(message, y=10, x=10):
    display_surf = pygame.display.get_surface()
    debug_surf = font.render(str(message), True, 'yellow')
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pygame.draw.rect(display_surf, 'black', debug_rect)
    display_surf.blit(debug_surf, debug_rect)