import time

from state import State, Battle


def run(igt: int):
    s = State(igt)

    # holding l/r into the world map
    for _ in range(13):
        s.rng.rand()

    try:

        # desert
        for _ in range(55):
            s.walk(4, 24, True)

        # desert edge
        for _ in range(12):
            s.rng.rand()

        # grass
        for _ in range(172):
            s.walk(4, 0, True)

        # beach
        for _ in range(10000):
            s.walk(4, 17, True)

        print("wtf")
    except Battle as b:
        # print(vars(b), vars(s), s.rng.idx)
        return b, s


n = 0

c = time.time()
for x in range(10000):
    b, s = run(x)
    if b.battle_id in {92, 93, 94}:
        n += 1

print(time.time() - c, n)
