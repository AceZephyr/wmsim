from utils import fromTimeFormat, toTimeFormat
from constants import GROUND_TYPE_IDS, REGION_IDS

from state import State, Battle

junon =     REGION_IDS.Junon.value

grass =     GROUND_TYPE_IDS.Grass.value
forest =    GROUND_TYPE_IDS.Forest.value
hillSide =  GROUND_TYPE_IDS.Hill_Side.value

yuffieEncId = -1
yuffieChance = 32   # 32/256 = 1/8 chance

def run(igt: int):
    s = State(igt)

    # Zolom ticks once before you start moving
    s.zolom_tick()

    # Hold Left coming out of the mines - Zolombox
    for _ in range(13):
        s.walk(junon, grass, lr=True, movement=False, zolombox=True)

    try:
        # Grass - Zolombox
        for _ in range(60):
            s.walk(junon, grass, lr=True, zolombox=True)

        # Mountain - Zolombox
        for _ in range(23):
            s.walk(junon, hillSide, lr=True, zolombox=True)

        # Grass - Zolombox
        for _ in range(108):
            s.walk(junon, grass, lr=True, zolombox=True)
            
        # Grass - No Zolombox
        for _ in range(52):
            s.walk(junon, grass, lr=True, zolombox=False)

        # Forest - No Zolombox
        for _ in range(1000): # 60 frames running across forest. Run left and right after entering forest
            s.walk(junon, forest, lr=True, zolombox=False, yuffie_chance=yuffieChance)

        # No encounter for this IGT and movement
        return None, s

    except Battle as b:
        return b, s

startTime = fromTimeFormat('2:27:22')
windowSize = 3 * 60
endTime = startTime + windowSize

bizHawkOffset = 4

arr = []
for x in range(startTime, endTime):
    b, s = run(x + bizHawkOffset)
    if b and b.battle_id == yuffieEncId:
        arr.append(x)
        print(toTimeFormat(x))

#print(arr)
