from copy import deepcopy

import tabulate

from constants import MINUTES, HOURS
from state import State, Battle
from util import format_igt

# Tiny Bronco initial spawn from Palmer fight -> Corel 0-encounters with menus

START_IGT = 2 * HOURS + 40 * MINUTES
END_IGT = 3 * HOURS + 00 * MINUTES
FILENAME = "bronco_to_corel.txt"

LOADING_TIME = 3
MAX_MENUS = 2

REGION = 4
GROUND = 0
ENCOUNTER_THRESHOLDS_TO_END = 33

LINES = {
    1: 511,
    2: 508,
    3: 505,
    4: 502
}


def search_igt(igt, bronco_increments, thresholds=ENCOUNTER_THRESHOLDS_TO_END):
    init_state = State(igt)
    for _ in range(bronco_increments):
        init_state.walk(REGION, GROUND, True, movement=False)
    init_state.vehicle_frac_reset()
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
    abs_frames = [enc_check * 17 + 47 for enc_check in enc_checks]
    abs_frames_start = [(enc_check - 1) * 17 + 48 for enc_check in window_starts]
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
    for line in sorted(LINES.keys()):
        encs, window_starts = search_igt(igt, LINES[line])
        if encs is None:
            continue
        arm_swings, arm_swings_abs, arm_swings_abs_start = construct_arm_swings(encs, window_starts)
        lengths_combined = [(window_starts[i], encs[i]) for i in range(len(encs))]
        arm_swings_abs_combined = [(arm_swings_abs_start[i], arm_swings_abs[i]) for i in range(len(arm_swings_abs))]
        out.append([igt, format_igt(igt - LOADING_TIME), line, lengths_combined, arm_swings, arm_swings_abs_combined])
    return out


def main():
    out = []
    for igt in range(START_IGT + LOADING_TIME, END_IGT + LOADING_TIME):
        result = run_for_igt(igt)
        for r in result:
            if len(r[-1]) <= MAX_MENUS:
                out.append(r)
    out.sort(key=lambda x: x[0])
    with open(FILENAME, 'w') as f:
        f.write(tabulate.tabulate(out))


if __name__ == '__main__':
    main()
