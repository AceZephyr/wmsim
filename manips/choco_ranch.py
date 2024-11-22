from state import State, Battle
import tabulate

from util import format_igt

# Chocobo from Chocobo Farm with menus

FILENAME = "choco_ranch.txt"
START_IGT = 1 * 60 * 60 + 30 * 60
END_IGT = 1 * 60 * 60 + 40 * 60

# 0 for pc, 3 for psx
LOADING_OFFSET = 3

MENU_FRAMES = {
    0: None,
    1: 55,
    1.5: 86,
    2: 118,
    2.5: 150,
    3: 182,
    3.5: 214,
    4: 246
}
CHOCOVAL = 8

REGION = 0x1
GROUND = 0x0


def run(igt: int, menu_on_frame):
    s = State(igt)
    s.chocoval = CHOCOVAL

    s.walk(REGION, GROUND, False, zolombox=True, movement=False)
    for _ in range(13):
        s.walk(REGION, GROUND, True, zolombox=True, chocotracks=True, movement=False)

    try:
        for frame in range(10000):
            if frame == menu_on_frame:
                if s.zolom_timer <= 24:
                    return None, None
                s.walk(REGION, GROUND, True, zolombox=True, chocotracks=True, movement=False)
                for _ in range(19):
                    s.walk(REGION, GROUND, False, zolombox=True, chocotracks=True, movement=False)
            else:
                s.walk(REGION, GROUND, True, zolombox=True, chocotracks=True, movement=True)

        print("wtf")
    except Battle as b:
        return b, s


def run_second(igt: int):
    for spin in MENU_FRAMES:
        b, s = run(igt, MENU_FRAMES[spin])
        if b and b.battle_id == 56:
            adj_igt_str = format_igt(igt - LOADING_OFFSET)
            best = (adj_igt_str, s.walkframes, igt, b.preempt, spin)
            return best
    return None


def main():
    arr = []
    for igt in range(START_IGT + LOADING_OFFSET, END_IGT + LOADING_OFFSET):
        rs = run_second(igt)
        if rs is not None:
            arr.append([igt, rs[0], rs[1], rs[2], rs[4], "Preempt" if rs[3] else ""])
    with open(FILENAME, 'w') as f:
        f.write(tabulate.tabulate(arr))


if __name__ == '__main__':
    main()
