import tabulate

from state import State, Battle
from util import format_igt, HOURS, MINUTES

REGION = 0x8
GROUND_TYPE = 0x0
END_DANGER = 22 * 512

FILENAME = "nibel_to_rocket_town.txt"
START_IGT = 2 * HOURS + 30 * MINUTES
END_IGT = 3 * HOURS + 00 * MINUTES

# 3 on PSX, 0 on PC
LOADING_TIME = 3

# PC:
# HOLD_INPUTS = [True]
# PSX:
HOLD_INPUTS = [True, False]
MAXMENUS = 2


def run(igt, hold, menus):
    s = State(igt)
    try:
        if hold:
            for _ in range(13):
                s.walk(REGION, GROUND_TYPE, True, movement=False)
        for _ in range(menus):
            s.walk(REGION, GROUND_TYPE, True, movement=False)
        while s.danger < END_DANGER:
            s.walk(REGION, GROUND_TYPE, True)
        return True
    except Battle:
        return False


def run_igt(igt):
    for menus in range(MAXMENUS + 1):
        for hold in HOLD_INPUTS:
            if run(igt, hold, menus):
                return [format_igt(igt - LOADING_TIME), "Hold" if hold else "Delay", menus]
    return None


def main():
    out = []
    for igt in range(START_IGT + LOADING_TIME, END_IGT + LOADING_TIME):
        ret = run_igt(igt)
        if ret is not None:
            out.append(ret)
    with open(FILENAME, "w") as f:
        f.write(tabulate.tabulate(out))


if __name__ == '__main__':
    main()
