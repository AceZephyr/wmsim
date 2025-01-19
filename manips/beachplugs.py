import tabulate

from constants import MINUTES, HOURS, Ground, Region
from state import State, Battle
from util import format_igt

# Beachplug manip: CC skip alignment, exit buggy, down -> down-right. Includes pruning.
# Developed by DashRetro, edited by AceZephyr

START_IGT = 2 * HOURS + 55 * MINUTES
END_IGT = 3 * HOURS + 10 * MINUTES
FILENAME = "beachplugs.txt"
LOADING_TIME = 5
MAX_MENUS = 3

REGION = Region.Gold_Saucer
GROUND_FRAMES = [28, 26, 29, 27, 30, 25, 31, 25, 31, 25, 30, 27, 30, 25, 31, 25, 31, 25, 33]
GROUND_TYPES = [Ground.Beach, Ground.Grass]


def run(igt, menus):
    s = State(igt)
    s.vehicle_frac_reset()
    try:
        for i in range(len(GROUND_FRAMES)):
            frames = GROUND_FRAMES[i]
            ground_type = GROUND_TYPES[i % len(GROUND_TYPES)]
            for f in range(frames):
                s.walk(REGION, ground_type, True, movement=menus <= 0)
                menus = max(0, menus - 1)
        return None, None
    except Battle as b:
        return b, s


def run_igt(igt):
    out = []
    for menus in range(MAX_MENUS + 1):
        b, s = run(igt, menus)
        if b is None or s is None:
            continue
        if b.battle_id == 92:
            out.append([igt, format_igt(igt - LOADING_TIME), menus, s.walkframes, 0, "3x"])
        elif b.battle_id == 93:
            out.append([igt, format_igt(igt - LOADING_TIME), menus, s.walkframes, 150, "4x"])
        elif b.battle_id == 94:
            out.append([igt, format_igt(igt - LOADING_TIME), menus, s.walkframes, -60, "SIDE"])
    return out


def prune(results):
    p = 0
    while p < (len(results) - 1):  # Prune each IGT for best-in-IGT
        if results[p][0] == results[p + 1][0]:  # Check if next manip is the same IGT
            nowpoints = results[p][3] + (results[p][2] * 30) + results[p][4]
            nextpoints = results[p + 1][3] + (results[p + 1][2] * 30) + results[p + 1][4]
            if nowpoints < nextpoints:
                results.pop(p + 1)
                p -= 1
            else:
                results.pop(p)
                p -= 1
        p += 1
    p = 1
    while p < (len(results)):  # Prune IGTs that are better waited past
        if p > 0:
            nowpoints = (results[p][0] * 30) + (results[p][2] * 30) + results[p][3] + results[p][4]
            prevpoints = (results[p - 1][0] * 30) + (results[p - 1][2] * 30) + results[p - 1][3] + results[p - 1][4]
            if nowpoints < prevpoints:
                results.pop(p - 1)
                p -= 2
        p += 1


def main():
    out = []
    for igt in range(START_IGT + LOADING_TIME, END_IGT + LOADING_TIME):
        out.extend(run_igt(igt))
    prune(out)
    for c in range(len(out)):
        out[c].pop(4)
    with open(FILENAME, "w") as f:
        f.write(tabulate.tabulate(out))


if __name__ == '__main__':
    main()
