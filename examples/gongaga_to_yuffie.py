# For importing from parent directory (so this works in the examples folder)
import os.path
import sys
directory = os.path.dirname(os.path.abspath("__file__"))
sys.path.append(directory)

from constants import GROUND_TYPE_IDS, REGION_IDS
from state import State, Battle
from utils import fromTimeFormat, toTimeFormat


gongaga =   REGION_IDS.Gongaga
grass =     GROUND_TYPE_IDS.Grass
jungle =    GROUND_TYPE_IDS.Jungle
yuffieEncId = -1
yuffieChance = 64   # 64/256 = 1/4 chance


def run(igt: int):
    s = State(igt)

    # Buffered movement doesn't increment fractions for 13 frames
    for _ in range(13):
        s.walk(gongaga, jungle, lr=True, movement=False)

    try:
        # Jungle while holding Left, Right, L1, or R1 the whole time
        # Hold Right + L1 while leaving, add Up when needed to circle around Gongaga (stay in jungle)
        for _ in range(1000):
            s.walk(gongaga, jungle, lr=True, yuffie_chance=yuffieChance)

        # No encounter for this IGT and movement
        return None, s

    except Battle as b:
        return b, s

startTime = fromTimeFormat('2:26:00')
windowSize = 2 * 60
endTime = startTime + windowSize

bizhawkOffset = 4

for igt in range(startTime, endTime):
    b, s = run(igt + bizhawkOffset)
    if b and b.battle_id == yuffieEncId:
        print(toTimeFormat(igt))
