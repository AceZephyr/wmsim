# Used ergonomy_joe's decompliation for a significantly more clean implementation.
# Tested rigorouisly against the old implementation (see wmrng_old.py)

class WorldMapRNG:
    def shuffle(self):
        for i in range(0x20):
            self.rng[i] ^= self.rng[i + 0x1e9]
        for i in range(0x20, 0x209):
            self.rng[i] ^= self.rng[i - 0x20]

    def srand(self, seed: int):
        buf = [0 for _ in range(521)]
        k = 0
        for i in range(0x11):
            for _ in range(0x20):
                seed = (seed * 0x5D588B65 + 1) & 0xFFFFFFFF
                k = (k >> 1) | (seed & 0x80000000)
            buf[i] = k & 0xFFFFFFFF
        buf[0x10] = ((buf[0x10] << 0x17) ^ (buf[0] >> 9) ^ buf[0xF]) & 0xFFFFFFFF
        for i in range(0x11, 0x209):
            buf[i] = ((buf[i - 0x11] << 0x17) ^ (buf[i - 0x10] >> 9) ^ buf[i - 1]) & 0xFFFFFFFF
        self.rng = [x & 0xFF for x in buf]
        self.shuffle()
        self.shuffle()
        self.shuffle()
        self.idx = 0x208

    def rand(self):
        self.idx += 1
        self.calls += 1
        if self.idx >= 521:
            self.shuffle()
            self.idx = 0
        return self.rng[self.idx]

    def __init__(self, igt: int):
        self.rng = None
        self.idx = 0
        self.calls = 0

        self.srand(igt)
