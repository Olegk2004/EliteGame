from seed import SeedType
from system_generator import makesystem
import settings
import numpy as np
from math import sqrt

PAIRS = "..LEXEGEZACEBISOUSESARMAINDIREA.ERATENBERALAVETIEDORQUANTEISRION"


class Galaxy:
    def __init__(self, w0, w1, w2):
        self.w0 = w0
        self.w1 = w1
        self.w2 = w2
        self.systems = []
        self.capitals = []
        self.matches = {}
        self.distance_limit = 65

    def make_systems(self):
        s = SeedType(self.w0, self.w1, self.w2)
        for i in range(256):
            system = makesystem(s)
            self.systems.append(system)

        np.random.seed(int(s.w0 + s.w2))  # Сид для воспроизведения генерации
        self.capitals = np.random.choice(self.systems, 21)

    def create_matches(self):
        for i in self.systems:
            self.matches[i] = []
            for j in self.systems:
                if i != j:
                    if i.distance_to(j) < (65 / sqrt(253 ** 2 + 253 ** 2) * sqrt(settings.MAP_WIDTH**2 + settings.MAP_HEIGHT ** 2)):
                        self.matches[i].append(j)
