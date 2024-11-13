from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import deepcopy

import tabulate

from state import State, Battle
from util import format_igt

# Midgar -> Chocobo Ranch 0-encounter with menus

FILENAME = "midgar_choco_0enc.txt"
START_IGT = 1 * 60 * 60 + 28 * 60 + 00
END_IGT = 1 * 60 * 60 + 29 * 60 + 00
MAX_WORKERS = 8

# 0 for PC, 3 for psx
LOADING_TIME = 3
MAXMENUS = 4

FRAMES_TO_ZOLOM_BOX = 140 + 17 + 17 + 8
FRAMES_IN_GRAY = 140 + (8 * 17)
FRAMES_TO_CHOCO_FARM_REGION = 755
FRAMES_TOTAL = 920


def start(state: State, left_frames: int, adj: int):
    try:
        menus = 0
        down_frames = 0
        if adj < 0:
            down_frames = abs(adj)
        elif adj > 0:
            menus = abs(adj)
        for _ in range(left_frames):
            state.walk(0x0, 0x9, True, zolombox=False, movement=True)

        for _ in range(down_frames):
            state.walk(0x0, 0x9, False, zolombox=False, movement=True)
        for _ in range(menus):
            state.walk(0x0, 0x9, True, zolombox=False, movement=False)
        for _ in range(FRAMES_TO_ZOLOM_BOX + left_frames - menus):
            state.walk(0x0, 0x9, True, zolombox=False)
        for _ in range(FRAMES_IN_GRAY - FRAMES_TO_ZOLOM_BOX):
            state.walk(0x0, 0x9, True, zolombox=True)
    except Battle:
        return None

    state_stack = [(
        deepcopy(state),  # the state
        (),  # position frames of menus
        FRAMES_IN_GRAY,  # current "position frame"
        0,  # cooldown frames until next allowed menu
        ()
    )]

    while len(state_stack) > 0:
        current_state, menu_frames_tuple, position_frame, menu_cooldown, rng_idx_tuple = state_stack.pop()
        try:
            while position_frame < FRAMES_TOTAL:
                current_zolom_timer = current_state.zolom_timer
                current_frac = current_state.frac
                current_state.walk(0x0, 0x0, True, zolombox=True)
                position_frame += 1
                if menu_cooldown > 0:
                    menu_cooldown -= 1
                    continue
                if current_state.zolom_timer <= 20 + 6:
                    continue
                if current_state.zolom_timer == current_zolom_timer - 1 and current_state.frac == current_frac + 1:
                    continue
                if len(menu_frames_tuple) >= MAXMENUS:
                    continue
                rngi = current_state.rng.idx
                new_state = deepcopy(current_state)
                new_state.walk(0x0, 0x0, True, zolombox=True, movement=False)
                for _ in range(19):  # menu fadeout
                    new_state.walk(0x0, 0x0, False, zolombox=True, movement=False)
                state_stack.append((
                    new_state,
                    menu_frames_tuple + (position_frame,),
                    position_frame + 1,
                    20,
                    rng_idx_tuple + (rngi,)
                ))
            return menu_frames_tuple, rng_idx_tuple
        except Battle:
            continue
    return None


def run(igt, left, adj):
    a = start(State(igt), left, adj)
    if a is None:
        return None
    menus, rng_idx = a
    return igt, format_igt(igt - LOADING_TIME), left, adj, menus, rng_idx


def run_for_igt(igt):
    out = []
    for left_frames in [0, 1, 2, 3, 4, 5, 6, 7]:
        out.append(run(igt, left_frames, 0))
        for menus in [1, 2, 3, 4, 5, 6, 7]:
            out.append(run(igt, left_frames, menus))
        for down_frames in [1, 2, 3, 4, 5, 6, 7]:
            out.append(run(igt, left_frames, -down_frames))
    return [x for x in out if x is not None]


def main():
    out = []
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for igt in range(START_IGT + LOADING_TIME, END_IGT + LOADING_TIME):
            futures.append(executor.submit(run_for_igt, igt))
        for future in as_completed(futures):
            result = future.result()
            if len(result) > 0:
                print(*result, sep='\n')
            out.extend(result)
    out.sort(key=lambda x: x[0])
    with open(FILENAME, "w") as f:
        f.write(tabulate.tabulate(out))


if __name__ == '__main__':
    main()
