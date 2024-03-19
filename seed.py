class FastSeedType:
    def __init__(self, a, b, c, d):
        self.a = a & 0xFF
        self.b = b & 0xFF
        self.c = c & 0xFF
        self.d = d & 0xFF


class SeedType:
    def __init__(self, w0, w1, w2):
        self.w0 = w0 & 0xFFFF
        self.w1 = w1 & 0xFFFF
        self.w2 = w2 & 0xFFFF
