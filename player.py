from random import choice
from settings import MAX_FUEL_VALUE


class Player:
    def __init__(self, galaxy):
        self.current_planet = choice(galaxy.systems)
        self.galaxy = galaxy
        self.fuel = 1000
        self.fuel_const = self.fuel  # Две строчки для полоски (сорри за такой стиль)
        self.bar_save = self.fuel
        self.visited_planets = [self.current_planet]
        self.display_mode = "map"
        self.current_planet.fuel_station_value = 0

    def jump(self, destination):
        now_distance = self.current_planet.distance_to(destination)
        if now_distance <= self.fuel:
            self.fuel -= now_distance
            self.fuel = min(self.fuel + destination.fuel_station_value, MAX_FUEL_VALUE)
            self.fuel -= destination.pirates_value
            destination.fuel_station_value = 0
            self.current_planet = destination
            self.visited_planets.append(destination)
            return True
        else:
            return False
