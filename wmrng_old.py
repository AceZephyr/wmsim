# Essentially a direct translation of the MIPS code for WM RNG on PSX.
# See wmrng.py for a better implementation that is actually used

def _scramble_rng(rng: list):
    a0 = 0
    while a0 < 0x20:
        v0 = rng[a0]
        v1 = rng[a0 + 489]
        v0 = v0 ^ v1
        rng[a0] = v0
        a0 += 1
    a0 = 0x20
    a1 = 0
    while a0 < 0x209:
        v0 = rng[a1]
        v1 = rng[a0]
        v0 = v0 ^ v1
        rng[a0] = v0
        a0 += 1
        a1 += 1
    return rng

def _seed_rng(igt: int):
    stack = []
    rng = []

    a0 = igt

    a3 = 0

    t0 = 0x5D588B65
    t1 = 0x80000000
    while len(stack) < 17:  # outer loop
        a1 = 31
        while a1 >= 0:  # inner loop
            a1 -= 1
            a0 = ((a0 * t0) + 1) % 2 ** 32
            v1 = a3 >> 1
            v0 = a0 & t1
            a3 = v1 | v0
        stack.append(a3)
    v0 = stack[-1]
    v1 = stack[0]
    a0 = stack[-2]
    v0 = (v0 << 0x17) % 2 ** 32
    v1 = v1 >> 9
    v0 = v0 ^ v1
    v0 = v0 ^ a0
    stack[-1] = v0
    a2 = 0x11
    a1 = 0
    while a2 < 0x209:
        a2 += 1
        v0 = stack[a1]
        v1 = stack[a1 + 1]
        a0 = stack[a1 + 16]
        v0 = (v0 << 0x17) % 2 ** 32
        v1 = v1 >> 9
        v0 = v0 ^ v1
        v0 = v0 ^ a0
        stack.append(v0)
        a1 += 1
    a2 = 0
    v1 = 0  # index
    while a2 < 0x209:
        v0 = stack[v1] % 2 ** 8
        rng.append(v0)
        a2 += 1
        v1 += 1
    rng = _scramble_rng(rng)
    rng = _scramble_rng(rng)
    rng = _scramble_rng(rng)
    return rng


class WorldMapRNG:

    def rand(self):
        self.idx += 1
        self.calls += 1
        if self.idx >= 521:
            self.rng = _scramble_rng(self.rng)
            self.idx = 0
        return self.rng[self.idx]

    def __init__(self, igt: int):
        self.rng = _seed_rng(igt)
        self.idx = 520
        self.calls = 0
