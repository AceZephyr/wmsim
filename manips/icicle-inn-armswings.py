from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import deepcopy

import tabulate

from state import State, Battle
from util import format_igt, HOURS, MINUTES

# CotA -> Icicle Inn 0-encounters

MAX_WORKERS = 8
START_IGT = 1 * HOURS + 50 * MINUTES
END_IGT = 2 * HOURS + 50 * MINUTES

FILENAME = "icicle-inn-armswings.txt"

LOADING_TIME = 3
MAX_MENUS = 4

REGION = 0xB
GROUND = 0xA
FRAMES_OF_MOVEMENT_TO_END = 880

START_CONDITIONS = list(range(-7, 7 + 1))


def search_igt(igt, hold_start: bool, start_condition: int):
    init_state = State(igt)
    frames = FRAMES_OF_MOVEMENT_TO_END
    if hold_start:
        frames -= 13
        for _ in range(13):
            init_state.walk(REGION, GROUND, True, movement=False)

    if start_condition > 0:
        # do menus
        for _ in range(abs(start_condition)):
            init_state.walk(REGION, GROUND, True, movement=False)
            frames -= 1
    elif start_condition < 0:
        # do down taps
        for _ in range(abs(start_condition)):
            init_state.walk(REGION, GROUND, False, movement=True)
            frames -= 1

    thresholds = (frames - 140) // 17
    while init_state.frac != 0:
        init_state.walk(REGION, GROUND, True)
    s = deepcopy(init_state)
    enc_checks = 0
    menus_list = []
    while enc_checks <= thresholds:
        menus = 0
        while True:
            s_copy = deepcopy(s)
            for _ in range(menus):
                s_copy.walk(REGION, GROUND, True, movement=False)
            try:
                while s_copy.frac == 0:
                    s_copy.walk(REGION, GROUND, True)
                while s_copy.frac != 0:
                    s_copy.walk(REGION, GROUND, True)
                break
            except Battle as b:
                menus += 1
                continue
        s = s_copy
        enc_checks += 1
        menus_list.append(menus)

    menu_times_list = flip(menus_list)

    if len(menu_times_list) > MAX_MENUS:
        return None, None

    window_start_list = []
    prev_min = 0
    state2 = deepcopy(init_state)
    for i in range(len(menu_times_list)):
        current_min = menu_times_list[i]
        while current_min > prev_min:
            state = deepcopy(state2)
            while state.encounter_checks < current_min - 1:
                state.walk(REGION, GROUND, True)
            state.walk(REGION, GROUND, True, movement=False)  # menu
            try:
                while state.encounter_checks < current_min:
                    state.walk(REGION, GROUND, True)
            except Battle:
                break
            current_min -= 1

        while state2.encounter_checks < current_min:
            state2.walk(REGION, GROUND, True)
        state2.walk(REGION, GROUND, True, movement=False)  # menu

        prev_min = current_min
        window_start_list.append(current_min)
    return menu_times_list, window_start_list


def flip(l):
    out = []
    for i in range(len(l)):
        for _ in range(l[i]):
            out.append(i)
    return out


def construct_arm_swings(enc_checks, window_starts):
    abs_frames = [enc_check * 17 + 157 for enc_check in enc_checks]
    abs_frames_start = [(enc_check - 1) * 17 + 158 for enc_check in window_starts]
    frames = []
    if len(abs_frames) > 0:
        frames.append(abs_frames[0] - 8)
    for i in range(1, len(abs_frames)):
        frames.append(abs_frames[i] - abs_frames[i - 1])
    return ([round(f / 15, 1) for f in frames],
            [round(f / 15, 1) for f in abs_frames],
            [round(f / 15, 1) for f in abs_frames_start])


def run_for_igt(igt: int):
    out = []
    for start_condition in START_CONDITIONS:
        for hold_start in [True, False]:
            encs, window_starts = search_igt(igt, hold_start, start_condition)
            if encs is None:
                continue
            arm_swings, arm_swings_abs, arm_swings_abs_start = construct_arm_swings(encs, window_starts)
            lengths_combined = [(window_starts[i], encs[i]) for i in range(len(encs))]
            arm_swings_abs_combined = [(arm_swings_abs_start[i], arm_swings_abs[i]) for i in range(len(arm_swings_abs))]
            out.append(
                [igt, format_igt(igt - LOADING_TIME), hold_start, start_condition, lengths_combined, arm_swings,
                 arm_swings_abs_combined])
    return out


def main():
    out = []
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = []
        for i in range(START_IGT + LOADING_TIME, END_IGT + LOADING_TIME):
            futures.append(executor.submit(run_for_igt, i))
        for future in as_completed(futures):
            result = future.result()
            if len(result) > 0:
                print(result[0][1])
            for r in result:
                if len(r[-1]) <= MAX_MENUS:
                    out.append(r)
    out.sort(key=lambda x: x[0])
    with open(FILENAME, "w") as f:
        f.write(tabulate.tabulate(out))


if __name__ == '__main__':
    main()
