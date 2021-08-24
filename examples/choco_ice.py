from state import State, Battle


def run(igt: int, start_hold: bool, menus: int):
    s = State(igt)
    s.chocoval = 12

    if start_hold:
        # holding l/r into the world map
        for _ in range(13):
            s.rng.rand()

    for _ in range(menus):
        s.rng.rand()

    try:

        # snow
        for _ in range(140 + 5 * 17):
            s.walk(0xB, 0xA, True, chocotracks=False)

        for _ in range(10000):
            s.walk(0xB, 0xA, True, chocotracks=True)

        print("wtf")
    except Battle as b:
        return b, s


def run_second(igt: int):
    best = None
    for start_hold in [True, False]:
        for menus in range(4):
            b, s = run(igt, start_hold, menus)
            if b.battle_id in {202, 203}:
                est_time = s.walkframes + (30 * menus) + (0 if start_hold else 30)
                if est_time < 600 and (best is None or best[5] > est_time):
                    best = (igt, start_hold, menus, b.battle_id, s.walkframes, est_time)
    return best


arr = []

for igt in range(12 * 60 * 60):
    rs = run_second(igt)
    if rs is not None:
        arr.append(",".join([str(a) for a in rs]) + "\n")
    if igt % (60 * 60) == 0:
        print(igt, len(arr))

with open("choco_ice.txt", "w") as file:
    file.writelines(arr)
