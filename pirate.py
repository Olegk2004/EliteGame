from random import choice


class Pirate:
    def __init__(self, galaxy):
        self.current_planet = choice(galaxy.systems)
        self.galaxy = galaxy
        self.fuel = 10000000000000
        self.visited_planets = [self.current_planet]
        self.wanna_visit = 0
        self.f = 0

    def jump(self, destination):
        now_distance = self.current_planet.distance_to(destination)
        if now_distance <= self.fuel:
            self.fuel -= now_distance
            self.fuel += destination.fuel_station_value
            destination.fuel_station_value = 0
            self.current_planet = destination
            self.visited_planets.append(destination)
            return True
        else:
            return False
    def wish(self):
        #match = choice(self.galaxy.matches[self.current_planet])
        for i in range(len(self.galaxy.matches[self.current_planet])):
            match = choice(self.galaxy.matches[self.current_planet])
            if match not in self.visited_planets:
                self.f = 1
                break
        if self.f == 0:
            self.wanna_visit = self.current_planet
        else:
            self.wanna_visit = match