import pygame
import galaxy


def draw(galaxy, surface):
    # sky_surface = pygame.display.get_surface()
    for system in galaxy.systems:
        pygame.draw.circle(surface, [0, 255, 0], (system.x, system.y), 2)
