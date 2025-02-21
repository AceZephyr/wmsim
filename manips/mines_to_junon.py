import copy

import tabulate

from constants import HOURS, MINUTES
from state import State, Battle
from util import format_igt

MAXMENUS_PER_STEP = 3

REGION = 0x2
GROUND = 0x0

START_IGT = 2 * HOURS + 0 * MINUTES
END_IGT = 2 * HOURS + 30 * MINUTES

MAX_MENUS_ALLOWED = 2
LOADING_OFFSET = 3


def search_igt(igt, frames_in_zolom, thresholds):
    init_state = State(igt)
    # initialize zolom
    init_state.walk(REGION, GROUND, False, movement=False, zolombox=True)
    for _ in range(13):
        init_state.walk(REGION, GROUND, True, movement=False, zolombox=True)
    try:
        for _ in range(frames_in_zolom):
            init_state.walk(REGION, GROUND, True, movement=True, zolombox=True)
    except Battle:
        return None, None
    s = copy.deepcopy(init_state)
    enc_checks = 0
    menus_list = [0 for _ in range(s.encounter_checks)]
    while enc_checks <= thresholds:
        menus = 0
        while True:
            s_copy = copy.deepcopy(s)
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

    if len(menu_times_list) > MAX_MENUS_ALLOWED:
        return None, None

    window_start_list = []
    state2 = copy.deepcopy(init_state)
    starting_enc_checks = state2.encounter_checks
    prev_min = starting_enc_checks
    for i in range(len(menu_times_list)):
        current_min = menu_times_list[i]
        while current_min > prev_min:
            state = copy.deepcopy(state2)
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


def run_for_igt_pattern(igt: int, pattern_key):
    out = []
    pattern = PATTERNS[pattern_key]
    encs, window_starts = search_igt(igt, pattern["framesZolom"], pattern["encChecksTotal"])
    if encs is None:
        return None
    arm_swings, arm_swings_abs, arm_swings_abs_start = construct_arm_swings(encs, window_starts)
    lengths_combined = [(window_starts[i], encs[i]) for i in range(len(encs))]
    arm_swings_abs_combined = [(arm_swings_abs_start[i], arm_swings_abs[i]) for i in range(len(arm_swings_abs))]
    out.append(
        [igt, format_igt(igt - LOADING_OFFSET), pattern_key, lengths_combined, arm_swings, arm_swings_abs_combined])
    return out


D = 17 + 140


def construct_arm_swings(enc_checks, window_starts):
    abs_frames = [enc_check * 17 + D for enc_check in enc_checks]
    abs_frames_start = [(enc_check - 1) * 17 + D + 1 for enc_check in window_starts]
    frames = []
    if len(abs_frames) > 0:
        frames.append(abs_frames[0] - 8)
    for i in range(1, len(abs_frames)):
        frames.append(abs_frames[i] - abs_frames[i - 1])
    return ([round(f / 15, 1) for f in frames],
            [round(f / 15, 1) for f in abs_frames],
            [round(f / 15, 1) for f in abs_frames_start])


def flip(l):
    out = []
    for i in range(len(l)):
        for _ in range(l[i]):
            out.append(i)
    return out


PATTERNS = {
    'low': {  # LOW pattern (100% consistent last zolom frame)
        "framesTotal": 740,  # total frames to reach junon
        "framesZolom": 140 + 13 + 17 + 17 + 17 + 1 - 15,  # total frames within zolom box
        "encChecksTotal": 30
    },
    'high': {  # HIGH pattern (inconsistent last zolom frame, may matter sometimes)
        "framesTotal": 740,  # total frames to reach junon
        "framesZolom": 140 + 13 + 17 + 17 + 17 + 17 + 8 - 17,  # total frames within zolom box
        "encChecksTotal": 30
    }
}


def main():
    out = []
    for igt in range(2 * 60 * 60 + 0 * 60 + LOADING_OFFSET, 2 * 60 * 60 + 30 * 60 + LOADING_OFFSET):
        for pattern_key in PATTERNS.keys():
            result = run_for_igt_pattern(igt, pattern_key)
            if result is None:
                continue
            for r in result:
                if len(r[-1]) <= MAX_MENUS_ALLOWED:
                    out.append(r)
    out.sort(key=lambda x: x[0])
    print(tabulate.tabulate(out))


if __name__ == '__main__':
    main()
