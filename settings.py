import pygame

SCREEN_WIDTH = 1050
SCREEN_HEIGHT = 750
MAP_WIDTH = 3000
MAP_HEIGHT = 3000
MAP_PANEL_WIDTH = 750
MAP_PANEL_HEIGHT = 750
EDGES_COLOR = [255, 255, 0]
CURRENT_PLANET_IMAGE = pygame.image.load("Images/Current_Planet.png")
STANDART_PLANET_IMAGE = pygame.image.load("Images/Standard_Planet.png")
CAPITAL_PLANET_IMAGE = pygame.image.load("Images/Capital_Planet.png")
FUEL_STATION_PLANET_IMAGE = pygame.image.load("Images/Fuel_Planet.png")
SUPER_FUEL_PLANET_IMAGE = pygame.image.load("Images/Super_Fuel.png")
# PLAYER_IMAGE = pygame.image.load("Images/7rb7.gif")
FUEL_CONST = 2500
MAX_FUEL_VALUE = int(FUEL_CONST * 1.48)
FPS = 220
