from random import choice


class Player:
    def __init__(self, galaxy):
        self.current_planet = choice(galaxy.systems)
        self.galaxy = galaxy
        self.fuel = 1000

    def jump(self, destination):
        now_distance = self.current_planet.distance_to(destination)
        if now_distance <= self.fuel:
            self.fuel -= now_distance
            self.current_planet = destination
            return True
        else:
            return False

