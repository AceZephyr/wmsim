from utils import fromTimeFormat, toTimeFormat
from constants import GROUND_TYPE_IDS, REGION_IDS

from state import State, Battle

def run(igt: int):
    s = State(igt)

    try:
        # Drive down and up after leaving Gold Saucer
        # Doesn't matter if you buffer the input or not
        # Don't touch the desert edge
        for _ in range(10000):
            s.walk(REGION_IDS.Gold_Saucer.value, GROUND_TYPE_IDS.Gold_Saucer_Desert.value, False)

        # No encounter for this IGT and movement
        return None, s

    except Battle as b:
        return b, s


startTime = fromTimeFormat('2:26:00')
windowSize = 2 * 60
endTime = startTime + windowSize

harpyId = 106
bizHawkOffset = 4

arr = []
for x in range(startTime, endTime):
    b, s = run(x + bizHawkOffset)
    if b and b.battle_id == harpyId:
        arr.append(x)
        print(toTimeFormat(x))

# print(arr)