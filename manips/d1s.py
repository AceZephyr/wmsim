from copy import deepcopy

from state import State, Battle
from wmrng import WorldMapRNG
from util import format_igt, HOURS, MINUTES

# Disc 1 Skip (from Kalm. https://youtu.be/WYXqVmjhZco)

FILENAME = "d1s.txt"
START_IGT = 1 * HOURS + 30 * MINUTES
END_IGT = 2 * HOURS + 30 * MINUTES

INITIAL_RNG = 1439

T4_1_UP = 18
T4_2_LEFT_FOREST = 129  # rot 0 dismount
T4_3_LEFT_GRASS = 118  # rot 0 dismount
T4_4_UP = 2
T4_5_RIGHT_GRASS = 117
T4_6_RIGHT_FOREST = 125  # 1d1d chocobo entry
T4_7_DOWN = 9

C4_RNG = 305

T5_1_UP = 18
T5_2_LEFT_FOREST = 129  # from x = 0x1e5f
T5_3_LEFT_GRASS = 57
T5_4_UP = 18
T5_5_LEFT_GRASS = 77
T5_6_DOWN = 18
T5_7_RIGHT_GRASS = 133
T5_8_RIGHT_FOREST = 124  # 1d06 chocobo entry
T5_9_DOWN = 9

C5_RNG = 323

DISTANCE_TO_COTA = 491


# Searches for menu pattern to get through a given state
def search_menus(initial_state: State, frames: int, max_menus=50):
    initial_state.movement_frames = 0
    s = deepcopy(initial_state)

    menu_frames = []
    while s.movement_frames < frames:
        if s.frac < 16:
            try:
                s.walk(0, 0, True)
                s.movement_frames += 1
            except Battle:
                raise Exception("should never happen")
            continue

        s_peek = deepcopy(s)
        try:
            s_peek.walk(0, 0, True)
            s_peek.movement_frames += 1
            s = s_peek
        except Battle:
            try:
                s.walk(0, 0, True, movement=False)
                s.movement_frames += 1
            except Battle:
                breakpoint()  # something unexpected has happened!
                raise Exception()
            menu_frames.append(s.movement_frames)
        if len(menu_frames) > max_menus:
            return None, None

    window_start_list = []
    no_menu_state = deepcopy(initial_state)
    no_menu_state.movement_frames = 0
    prev_min = -1

    for i in range(len(menu_frames)):
        current_min = prev_min + 1
        menu_state = deepcopy(no_menu_state)
        try:
            menu_state.walk(0, 0, lr=True, movement=False)
            menu_state.movement_frames += 1
        except Battle:
            breakpoint()  # something unexpected has happened!
            raise Exception()
        last_good_menu_state = deepcopy(menu_state)

        while no_menu_state.movement_frames < menu_frames[i] - 1:
            try:
                menu_state.walk(0, 0, True)
                menu_state.movement_frames += 1
            except Battle:
                try:
                    no_menu_state.walk(0, 0, True)
                    no_menu_state.movement_frames += 1
                except Battle:
                    breakpoint()  # something unexpected has happened!
                    raise Exception()
                current_min = no_menu_state.movement_frames
                menu_state = deepcopy(no_menu_state)
                try:
                    menu_state.walk(0, 0, lr=True, movement=False)
                    menu_state.movement_frames += 1
                except Battle:
                    breakpoint()  # something unexpected has happened!
                    raise Exception()
                last_good_menu_state = deepcopy(menu_state)
                continue
            try:
                no_menu_state.walk(0, 0, True)
                no_menu_state.movement_frames += 1
            except Battle:
                breakpoint()  # something unexpected has happened!
                raise Exception()

        window_start_list.append(current_min)
        no_menu_state = last_good_menu_state
        prev_min = current_min

    return menu_frames, window_start_list


def perform_menus(menu_walkframes, state, distance_frames):
    menu_walkframes = sorted(menu_walkframes)[::-1]
    f = 0
    try:
        while f < distance_frames:
            if len(menu_walkframes) > 0 and menu_walkframes[-1] - 1 == f:
                menu_walkframes.pop(-1)
                state.walk(0, 0, True, movement=False)
            else:
                state.walk(0, 0, True)
            f += 1
        return state
    except Battle:
        return None


def combine(window_start_frames, menu_frames):
    if len(menu_frames) != len(window_start_frames):
        raise Exception()
    return [(window_start_frames[i], menu_frames[i]) for i in range(len(menu_frames))]


def print_step_graph(state: State, enc_checks: int, width=50, danger_increase=512):
    CHR_ENC = "X"
    CHR_NOENC = "."
    CONST = 18
    r = deepcopy(state.rng)
    init_danger = state.danger
    for _ in range(17 - state.frac):
        r.rand()
    arr = [[None for _ in range(width)] for _ in range(enc_checks)]

    for i in range(CONST * enc_checks + width):
        rval = r.rand()
        j = i
        while j >= 0:
            if j < width and (i - j) // CONST < enc_checks:
                arr[(i - j) // CONST][j] = rval < ((((i - j) // CONST + 1) * danger_increase + init_danger) >> 8)
            j -= CONST

    for arr2 in arr:
        print("".join(CHR_ENC if elem else CHR_NOENC for elem in arr2))


def remove_none_values(dict_in: dict):
    return {k: dict_in[k] for k in dict_in if dict_in[k] is not None}


def run_for_igt(igt: int):
    T4_START_STANDARD_ABSOLUTE_COUNT = 1439
    T4_START_STANDARD_DANGER = 0
    T5_START_STANDARD_ABSOLUTE_COUNT = 2246
    T5_START_STANDARD_DANGER = 13 * 512
    END_START_STANDARD_ABSOLUTE_COUNT = 3106
    END_START_STANDARD_DANGER = 30 * 512

    t4_data = {}
    t5_data = {}
    end_data = {}
    for t4_count in range(-8, 9):
        t4_data[t4_count] = None
        s = State(igt)
        s.danger = T4_START_STANDARD_DANGER
        for _ in range(T4_START_STANDARD_ABSOLUTE_COUNT + t4_count):
            s.rng.rand()

        s.vehicle_frac_reset()
        for _ in range(T4_1_UP):
            s.walk(0, 0, lr=False, movement=True)
        for _ in range(T4_2_LEFT_FOREST):
            s.walk(0, 0, lr=True, movement=False)

        # t4_3_state = deepcopy(s)
        t4_3_menu_frames, t4_3_window_starts = search_menus(s, T4_3_LEFT_GRASS, max_menus=3)
        if t4_3_menu_frames is None:
            continue
        s = perform_menus(t4_3_menu_frames, s, T4_3_LEFT_GRASS)
        assert s is not None

        try:
            for _ in range(T4_4_UP):
                s.walk(0, 0, lr=False, movement=True)
        except Battle:
            breakpoint()  # something unexpected has happened!

        # t4_5_state = deepcopy(s)
        t4_5_menu_frames, t4_5_window_starts = search_menus(s, T4_5_RIGHT_GRASS)
        if t4_5_menu_frames is None:
            return None
        s = perform_menus(t4_5_menu_frames, s, T4_5_RIGHT_GRASS)
        assert s is not None

        for _ in range(T4_6_RIGHT_FOREST):
            s.walk(0, 0, lr=True, movement=False)
        try:
            for _ in range(T4_7_DOWN):
                s.walk(0, 0, lr=False, movement=True)
        except Battle:
            t4_data[t4_count] = None
            continue
        t4_data[t4_count] = (
            combine(t4_3_window_starts, t4_3_menu_frames),
            combine(t4_5_window_starts, t4_5_menu_frames)
        )

    t5_up_safe_values = set()
    t5_up_safe_values_2 = dict()
    for t5_up_value in range(-12, 12 + 6 + 1):
        r = WorldMapRNG(igt)
        for _ in range(T5_START_STANDARD_ABSOLUTE_COUNT + T5_2_LEFT_FOREST + T5_3_LEFT_GRASS + t5_up_value + 2):
            r.rand()
        r1 = r.rand()
        r2 = r.rand()
        if r1 >= (8192 >> 8) and r2 >= (8704 >> 8):
            t5_up_safe_values.add(t5_up_value)

    t5_three_menu_safe_counts = []
    for t5_count in range(-12, 13):
        r = WorldMapRNG(igt)
        for _ in range(2782 + t5_count):
            r.rand()
        r1 = r.rand()
        if r1 >= (15360 >> 8):
            t5_three_menu_safe_counts.append(t5_count)

    for t5_count in range(-12, 13):
        t5_data[t5_count] = None
        s = State(igt)
        s.danger = T5_START_STANDARD_DANGER
        for _ in range(T5_START_STANDARD_ABSOLUTE_COUNT + t5_count):
            s.rng.rand()

        s.vehicle_frac_reset()
        for _ in range(T5_1_UP):
            s.walk(0, 0, lr=False, movement=True)
        for _ in range(T5_2_LEFT_FOREST):
            s.walk(0, 0, lr=True, movement=False)

        # t5_3_state = deepcopy(s)
        t5_3_menu_frames, t5_3_window_starts = search_menus(s, T5_3_LEFT_GRASS, max_menus=5)
        if t5_3_menu_frames is None:
            continue
        s = perform_menus(t5_3_menu_frames, s, T5_3_LEFT_GRASS)
        assert s is not None

        t5_5_states = []
        t5_4_state = None

        # before_up_state = deepcopy(s)

        # go from the end
        for t5_up_value in reversed(range(7)):
            # if t5_up_value + t5_count not in t5_up_safe_values:
            #     continue

            t5_4_state = deepcopy(s)
            try:
                for _ in range(t5_up_value):
                    t5_4_state.walk(0, 0, lr=True)
            except Battle:
                continue
            try:
                for _ in range(T5_4_UP):
                    t5_4_state.walk(0, 0, lr=False, movement=True)
            except Battle:
                continue
            try:
                for _ in range(6 - t5_up_value):
                    t5_4_state.walk(0, 0, lr=True)
            except Battle:
                continue
            if t5_count in t5_up_safe_values_2:
                t5_up_safe_values_2[t5_count].append(t5_up_value)
            else:
                t5_up_safe_values_2[t5_count] = [t5_up_value]
            t5_5_states.append(t5_4_state)

        if t5_4_state is None or len(t5_5_states) == 0:
            continue

        # sanity checking
        assert len(set(state.frac for state in t5_5_states)) == 1
        assert len(set(state.rng.idx for state in t5_5_states)) == 1

        s = t5_4_state

        t5_5_menu_frames, t5_5_window_starts = search_menus(s, T5_5_LEFT_GRASS - 6, max_menus=3)
        if t5_5_menu_frames is None:
            continue
        s = perform_menus(t5_5_menu_frames, s, T5_5_LEFT_GRASS - 6)
        assert s is not None

        try:
            for _ in range(T5_6_DOWN):
                s.walk(0, 0, lr=False, movement=True)
        except Battle:
            continue

        # t5_7_state = deepcopy(s)
        t5_7_menu_frames, t5_7_window_starts = search_menus(s, T5_7_RIGHT_GRASS, max_menus=6)
        if t5_7_menu_frames is None:
            continue
        s = perform_menus(t5_7_menu_frames, s, T5_7_RIGHT_GRASS)
        assert s is not None

        if len(t5_3_menu_frames) + len(t5_5_menu_frames) + len(t5_7_menu_frames) > 8:
            continue  # for now do not include solutions with more than 3 menus total.

        for _ in range(T5_8_RIGHT_FOREST):
            s.walk(0, 0, lr=True, movement=False)

        try:
            for _ in range(T5_9_DOWN):
                s.walk(0, 0, lr=False, movement=True)
        except Battle:
            continue

        t5_data[t5_count] = (
            combine(t5_3_window_starts, t5_3_menu_frames),
            combine(t5_5_window_starts, t5_5_menu_frames),
            combine(t5_7_window_starts, t5_7_menu_frames)
        )

    for end_count in range(-12, 18):
        end_data[end_count] = None
        s = State(igt)
        s.danger = END_START_STANDARD_DANGER
        for _ in range(END_START_STANDARD_ABSOLUTE_COUNT + end_count):
            s.rng.rand()

        s.vehicle_frac_reset()
        # end_state = deepcopy(s)
        end_menu_frames, end_window_starts = search_menus(s, DISTANCE_TO_COTA)
        if end_menu_frames is None:
            continue
        s = perform_menus(end_menu_frames, s, DISTANCE_TO_COTA)
        assert s is not None

        end_data[end_count] = combine(end_window_starts, end_menu_frames)

    return (remove_none_values(t4_data),
            t5_up_safe_values,
            t5_up_safe_values_2,
            t5_three_menu_safe_counts,
            remove_none_values(t5_data),
            remove_none_values(end_data))


def main():
    with open(FILENAME, "w") as file:
        file.write("")
    for igt in range(START_IGT, END_IGT):
        ret = run_for_igt(igt)
        if ret is None:
            continue
        t4_data, t5_up_safe_values, t5_up_safe_values_2, t5_three_menu_safe_counts, t5_data, end_data = ret
        mins = []
        min_pos = 0
        min_all = -12
        opt_pos = 0
        opt_all = -12
        for f in end_data:
            if f + 1 not in end_data.keys() or len(end_data[f]) <= len(end_data[f + 1]):
                mins.append(f)
            if f >= 0:
                if len(end_data[f]) < len(end_data[min_pos]):
                    min_pos = f
                if f + 2 * len(end_data[f]) < opt_pos + 2 * len(end_data[opt_pos]):
                    opt_pos = f
            if len(end_data[f]) < len(end_data[min_all]):
                min_all = f
            if abs(f) + 2 * len(end_data[f]) < abs(opt_all) + 2 * len(end_data[opt_all]):
                opt_all = f
        with open(FILENAME, "a") as file:
            file.write(f"""{igt}, {format_igt(igt)}

Min: {min_pos}: {len(end_data[min_pos])} ({min_all}: {len(end_data[min_all])})
Opt: {opt_pos}: {len(end_data[opt_pos])} ({opt_all}: {len(end_data[opt_all])})

t4: {t4_data}

t5 up-vals: {sorted(t5_up_safe_values)}

full t5 up-vals: {t5_up_safe_values_2}

t5 3-menu safe counts: {t5_three_menu_safe_counts}

t5: {t5_data}

end: {end_data}

Mins:
""")
            for m in mins:
                file.write(f"{m} {len(end_data[m])} {end_data[m]}\n")
            file.write(f"{'-' * 80}\n")
        print(igt, format_igt(igt))


if __name__ == '__main__':
    main()
