import pygame
import galaxy
import settings


def draw(galaxy, surface):
    # sky_surface = pygame.display.get_surface()
    for system in galaxy.systems:
        x = system.x / 260 * settings.SCREEN_WIDTH + 5
        y = system.y / 260 * settings.SCREEN_HEIGHT + 5
        pygame.draw.circle(surface, [0, 255, 0], (x, y), 4)
    for match in galaxy.matches:
        curr_x = match.x / 260 * settings.SCREEN_WIDTH + 5
        curr_y = match.y / 260 * settings.SCREEN_HEIGHT + 5
        for i in galaxy.matches[match]:
            match_x = i.x / 260 * settings.SCREEN_WIDTH + 5
            match_y = i.y / 260 * settings.SCREEN_HEIGHT + 5
            pygame.draw.line(surface, settings.EDGES_COLOR, (curr_x, curr_y), (match_x, match_y), 1)
