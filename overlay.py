import pygame
from settings import *


class Overlay:
    def __init__(self, display_surface, planet_player):
        self.display_surface = display_surface
        self.planet_player = planet_player
        # overlay_path = ''
        self.tools_surf = self.planet_player.tools_sprites

    def display(self):
        tool_surf = self.tools_surf[self.planet_player.selected_tool]
        tool_rect = tool_surf.get_rect(topleft=(10, 10))
        self.display_surface.blit(tool_surf, tool_rect)

        hp_bar_bgd = pygame.Surface((500, 20))
        hp_bar_bgd.fill('black')
        hp_bar = pygame.Surface((self.planet_player.hp / self.planet_player.max_hp * 500, 20))
        hp_bar.fill('red')
        hp_bar_bgd_rect = hp_bar_bgd.get_rect(topleft=(70, 10))
        hp_bar_rect = hp_bar.get_rect(topleft=(70, 10))
        self.display_surface.blit(hp_bar_bgd, hp_bar_bgd_rect)
        self.display_surface.blit(hp_bar, hp_bar_rect)

        stamina_bar_bgd = pygame.Surface((250, 20))
        stamina_bar_bgd.fill('black')
        stamina_bar = pygame.Surface((self.planet_player.stamina / self.planet_player.max_stamina * 250, 20))
        stamina_bar.fill('blue')
        stamina_bar_bgd_rect = stamina_bar_bgd.get_rect(topleft=(70, 40))
        stamina_bar_rect = stamina_bar.get_rect(topleft=(70, 40))
        self.display_surface.blit(stamina_bar_bgd, stamina_bar_bgd_rect)
        self.display_surface.blit(stamina_bar, stamina_bar_rect)

        if self.planet_player.hp <= 0:
            self.planet_player.timers['you died'].activate()
            you_died_font = pygame.font.SysFont('Century Gothic', 75, True)
            you_died_txt = you_died_font.render("YOU DIED", False, (255, 0, 0))
            you_died_rect = you_died_txt.get_rect()
            if self.planet_player.timers['you died'].active:
                you_died_txt.set_alpha(min(200, self.planet_player.timers['you died'].time_left() * 0.5))
                self.display_surface.blit(you_died_txt,
                                 (SCREEN_WIDTH // 2 - you_died_rect.width // 2,
                                  SCREEN_HEIGHT // 2 - 100))
