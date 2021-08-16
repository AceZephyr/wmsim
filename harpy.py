import time

from state import State, Battle


def run(igt: int):
    s = State(igt)

    try:

        # desert
        for _ in range(10000):
            s.walk(4, 24, False)

        print("wtf")
    except Battle as b:
        # print(vars(b), vars(s), s.rng.idx)
        return b, s


arr = []

c = time.time()
for x in range(10020, 10020 + 180):
    b, s = run(x+6)
    if b.battle_id == 107:
        # arr.append((x, b, s))
        arr.append(x)

print(arr)