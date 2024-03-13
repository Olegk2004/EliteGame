import pygame
import galaxy
import settings


def draw(galaxy, player, surface):
    # sky_surface = pygame.display.get_surface()
    for system in galaxy.systems:
        if system == player.current_planet:  # если это текущая планета игрока, то рисуем одним цветом
            pygame.draw.circle(surface, settings.CURRENT_PLANET_COLOR, (system.x, system.y), 5)
        elif system in player.visited_planets:  # если это посещенная планета, то другим
            pygame.draw.circle(surface, settings.VISITED_PLANETS_COLOR, (system.x, system.y), 3)
        else:
            pygame.draw.circle(surface, settings.UNVISITED_PLANETS_COLOR, (system.x, system.y), 3)
    for match in galaxy.matches[player.current_planet]:
        pygame.draw.line(surface, settings.EDGES_COLOR, (player.current_planet.x, player.current_planet.y),
                         (match.x, match.y), 1)
    '''
    for match in galaxy.matches:
        curr_x = match.x / 260 * settings.SCREEN_WIDTH + 5
        curr_y = match.y / 260 * settings.SCREEN_HEIGHT + 5
        for i in galaxy.matches[match]:
            match_x = i.x / 260 * settings.SCREEN_WIDTH + 5
            match_y = i.y / 260 * settings.SCREEN_HEIGHT + 5
            pygame.draw.line(surface, settings.EDGES_COLOR, (curr_x, curr_y), (match_x, match_y), 1)
    '''

def check_click(click_pos, player, galaxy):
    for planet in galaxy.matches[player.current_planet]:
        distance = ((planet.x - click_pos[0])**2 + (planet.y - click_pos[1])**2)**0.5  # Вычисляем расстояние между центром планеты и местом клика
        if distance < 4:  # Если клик произошел в пределах радиуса планеты
            return planet  # Возвращаем имя планеты
    return None