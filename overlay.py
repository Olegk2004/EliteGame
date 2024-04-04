import pygame
from settings import *

class Overlay:
    def __init__(self, display_surface, planet_player):
        self.display_surface = display_surface
        self.planet_player = planet_player
        # overlay_path = ''
        self.tools_surf = [pygame.surface.Surface((10, 10)), pygame.surface.Surface((10, 10))]
        self.tools_surf[0].fill('green') # Выбрана рука
        self.tools_surf[1].fill('pink') # Выбрана пушка

    def display(self):
        tool_surf = self.tools_surf[self.planet_player.tool_index]
        #tool_rect = tool_surf.get_rect(topleft=(self.planet_player.rect.topleft[0] - 5, self.planet_player.rect.topleft[1] - 5))
        #self.display_surface.blit(tool_surf, tool_rect)
