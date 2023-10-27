from utils import fromTimeFormat, toTimeFormat
from constants import GROUND_TYPE_IDS, REGION_IDS

from state import State, Battle

gongaga =   REGION_IDS["Gongaga"]

grass =     GROUND_TYPE_IDS["Grass"]
jungle =    GROUND_TYPE_IDS["Jungle"]

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
windowSize = 10 * 60
endTime = startTime + windowSize

arr = []
for x in range(startTime, endTime):
    b, s = run(x+4) # Use x+4 for bizhawk offset from menu close
    if b and b.battle_id == yuffieEncId:
        arr.append(x)
        print(toTimeFormat(x))

#print(arr)
