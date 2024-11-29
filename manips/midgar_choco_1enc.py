from concurrent.futures import ProcessPoolExecutor, as_completed

import tabulate

from state import State, Battle
from util import format_igt, HOURS, MINUTES

MAX_WORKERS = 8
FILENAME = "midgar_choco_1enc.txt"

START_IGT = 1 * HOURS + 20 * MINUTES
END_IGT = 1 * HOURS + 30 * MINUTES
MAXMENUS = 5

# 0 for PC, 3 for psx
LOADING_TIME = 0
WALKFRAMES_MIN = 700

# PROHIBITED_ENCOUNTERS = {43}
PROHIBITED_ENCOUNTERS = {}

FRAMES_TO_ZOLOM_BOX = 140 + 17 + 17 + 8
FRAMES_IN_GRAY = 140 + (8 * 17)
FRAMES_TO_CHOCO_FARM_REGION = 755


def run_left_menu(state: State, left_frames: int, menus: int):
    try:
        for _ in range(left_frames):
            state.walk(0x0, 0x9, True, zolombox=False, movement=True)
        for _ in range(menus):
            state.walk(0x0, 0x9, True, zolombox=False, movement=False)
        for _ in range(FRAMES_TO_ZOLOM_BOX + left_frames - menus):
            state.walk(0x0, 0x9, True, zolombox=False)
        for _ in range(FRAMES_IN_GRAY - FRAMES_TO_ZOLOM_BOX):
            state.walk(0x0, 0x9, True, zolombox=True)
        for _ in range(FRAMES_TO_CHOCO_FARM_REGION - FRAMES_IN_GRAY):
            state.walk(0x0, 0x0, True, zolombox=True)
        while True:
            state.walk(0x1, 0x0, True, zolombox=True)

    except Battle as battle:
        return battle, state


def run_left_down(state: State, left_frames: int, down_frames: int):
    try:
        for _ in range(left_frames):
            state.walk(0x0, 0x9, True, zolombox=False, movement=True)
        for _ in range(down_frames):
            state.walk(0x0, 0x9, False, zolombox=False, movement=True)
        for _ in range(FRAMES_TO_ZOLOM_BOX + left_frames):
            state.walk(0x0, 0x9, True, zolombox=False)
        for _ in range(FRAMES_IN_GRAY - FRAMES_TO_ZOLOM_BOX):
            state.walk(0x0, 0x9, True, zolombox=True)
        for _ in range(FRAMES_TO_CHOCO_FARM_REGION - FRAMES_IN_GRAY):
            state.walk(0x0, 0x0, True, zolombox=True)
        while True:
            state.walk(0x1, 0x0, True, zolombox=True)

    except Battle as battle:
        return battle, state


def run(igt, m1, m2, args):
    b, s = args
    if s.walkframes >= WALKFRAMES_MIN and b.battle_id not in PROHIBITED_ENCOUNTERS:
        return [igt, format_igt(igt - LOADING_TIME), m1, m2, s.walkframes, b.battle_id, "Preempt" if b.preempt else ""]
    return None


def run_for_igt(igt):
    out = []
    for left_frames in [0, 1, 2, 3, 4, 5, 6, 7]:
        out.append(run(igt, f"{left_frames}left", "0", run_left_menu(State(igt), left_frames, 0)))
        for menus in [1, 2, 3, 4, 5, 6, 7]:
            out.append(run(igt, f"{left_frames}left", f"{menus}menu", run_left_menu(State(igt), left_frames, menus)))
        for down_frames in [1, 2, 3, 4, 5, 6, 7]:
            out.append(run(igt, f"{left_frames}left", f"{down_frames}down",
                           run_left_down(State(igt), left_frames, down_frames)))
    return [x for x in out if x is not None]


def main():
    out = []
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for igt in range(START_IGT + LOADING_TIME, END_IGT + LOADING_TIME):
            futures.append(executor.submit(run_for_igt, igt))
        for future in as_completed(futures):
            out.extend(future.result())
    out.sort(key=lambda x: x[0])
    with open(FILENAME, 'w') as f:
        f.write(tabulate.tabulate(out))


if __name__ == '__main__':
    main()
