from state import State, Battle


def run(igt: int, start_hold: bool, menus: int):
    s = State(igt)

    # holding l/r into the world map
    if start_hold:
        for _ in range(13):
            s.walk(0x0, 0x0, True, movement=False, zolombox=False)

    for _ in range(menus):
        s.walk(0x0, 0x0, True, movement=False, zolombox=False)

    try:
        while s.walkframes < 140 + (-115):
            s.walk(0x0, 0x0, True, zolombox=False)

        while s.walkframes < 140 + (-101):
            s.walk(0x0, 0x9, True, zolombox=False)

        while s.walkframes < 140 + (-86):
            s.walk(0x0, 0x9, True, zolombox=True)

        while s.walkframes < 140 + 9:
            s.walk(0x0, 0x0, True, zolombox=True)

        while s.walkframes < 140 + (17 + 12):
            s.walk(0x0, 0x9, True, zolombox=True)

        while s.walkframes < 140 + (18 * 17 + 5):
            s.walk(0x0, 0x0, True, zolombox=True)

        for _ in range(10000):
            s.walk(0x1, 0x0, True, zolombox=True)

        print("wtf")
    except Battle as b:
        return b, s


for igt in range(2 * 60 * 60, 2 * 60 * 60 + 20 * 60):
    for start_hold in [True, False]:
        for menus in [0, 1, 2, 3, 4, 5]:
            b, s = run(igt, start_hold, menus)
            print(igt, start_hold, menus, s.walkframes, b.battle_id, b.preempt, sep=',')

# run(8000, True, 0)