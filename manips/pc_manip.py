import tabulate

from constants import HOURS, MINUTES, Ground, Region
from state import State, Battle
from util import format_igt

FILENAME = "pc_manip.txt"
START_IGT = 1 * HOURS
END_IGT = 2 * HOURS + 30 * MINUTES
MORE_THAN_ONE_PARTY_MEMBER = True

LOADING_TIME = 2

TARGET_ENCOUNTERS = {65}


def run(igt: int, lr: bool):
    s = State(igt, zolombox_init=True, more_than_one_party_member=MORE_THAN_ONE_PARTY_MEMBER)
    for _ in range(13):
        s.walk(Region.Junon, Ground.Grass, lr, zolombox=True, movement=False)
    try:
        for _ in range(100000):
            s.walk(Region.Junon, Ground.Grass, lr, zolombox=True)
        print("wtf")
    except Battle as b:
        return b, s


def main():
    out = []
    for igt in range(START_IGT + LOADING_TIME, END_IGT + LOADING_TIME):
        b, s = run(igt, True)
        if b.battle_id in TARGET_ENCOUNTERS:
            out.append((igt, format_igt(igt - LOADING_TIME), "Left+L1"))
            continue
        b, s = run(igt, False)
        if b.battle_id in TARGET_ENCOUNTERS:
            out.append((igt, format_igt(igt - LOADING_TIME), "Up/Down"))
            continue
    with open(FILENAME, "w") as f:
        f.write(tabulate.tabulate(out))


if __name__ == '__main__':
    main()
