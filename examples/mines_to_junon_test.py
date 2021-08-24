from state import State, Battle


def run(igt: int):
    s = State(igt)

    # holding l/r into the world map
    for _ in range(13):
        s.zolom_tick()
        s.rng.rand()

    try:
        for _ in range(140 + 17 + 17 + 17 + 1):
            s.walk(0x2, 0x0, True, zolombox=True)

        for _ in range(1000):
            s.walk(0x2, 0x0, True, zolombox=False)

        print("wtf")
    except Battle as b:
        # print(vars(b), vars(s), s.rng.idx)
        return b, s


b, s = run(308 + 4)
print(s.walkframes, b.battle_id)
