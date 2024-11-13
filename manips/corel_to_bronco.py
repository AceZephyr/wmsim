from copy import deepcopy

import tabulate

from state import State, Battle
from util import format_igt

# Corel -> Tiny Bronco 0-encounter with menus

START_IGT = 2 * 60 * 60 + 40 * 60
END_IGT = 2 * 60 * 60 + 55 * 60
FILENAME = "corel_to_bronco.txt"

MAX_MENUS = 2
LOADING_TIME = 3

REGION = 4
GROUND = 0
ENCOUNTER_THRESHOLDS_TO_END = 27


def search_igt(igt, thresholds=ENCOUNTER_THRESHOLDS_TO_END):
    init_state = State(igt)
    # 13 free frames
    for _ in range(13):
        init_state.walk(REGION, GROUND, True, movement=False)
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
    encs, window_starts = search_igt(igt)
    if encs is None:
        return None
    arm_swings, arm_swings_abs, arm_swings_abs_start = construct_arm_swings(encs, window_starts)
    lengths_combined = [(window_starts[i], encs[i]) for i in range(len(encs))]
    arm_swings_abs_combined = [(arm_swings_abs_start[i], arm_swings_abs[i]) for i in range(len(arm_swings_abs))]
    return igt, format_igt(igt - LOADING_TIME), lengths_combined, arm_swings, arm_swings_abs_combined


def main():
    out = []
    for igt in range(START_IGT, END_IGT):
        result = run_for_igt(igt)
        if result is not None and len(result[-1]) <= MAX_MENUS:
            out.append(result)
    out.sort(key=lambda x: x[0])
    with open(FILENAME, 'w') as f:
        f.write(tabulate.tabulate(out))


if __name__ == '__main__':
    main()
