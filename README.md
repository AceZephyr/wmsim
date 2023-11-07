# WMSim - FF7 World Map Simulator

WMSim is a tool for simulating battles RNG on the world map in Final Fantasy VII.

World map encounter RNG is seeded by the in-game-time (IGT) when the world map is loaded. Other factors affect these RNG values while on the world map such as inputs and the Midgar Zolom.

You can use WMSim to find IGTs that result in getting zero encounters while crossing the world map or to find specific encounter formations (which enemies are in the battle).

## Getting Started

WMSim provides the framework for writing simulation scripts to manipulate RNG on the world map. The framework and scripts are written in Python. 

1. Install Python 3
2. Install VSCode (or your preferred IDE or rich text editor)
3. Install the Python extension for your editor
4. Download or clone this repository and open it in your editor
5. Open `examples/harpy.py` and run the script (Ctrl+F5 in VSCode). This is a simple example of a simulation script
6. The script's output is a list of IGTs that result in encountering a Harpy when leaving Corel Prison in the buggy and moving only up and down in the desert

## Anatomy of Simulation Script

At the bottom of `harpy.py` is the main body of the script. It defines a `startTime` and `endTime` as IGTs (in total seconds) and runs `run()` for each. **These IGTs represent the time the world map is loaded** so there is often an "offset" for the time it takes to close the menu, zone out of a field map, and load the world map.

```python
startTime = fromTimeFormat('2:26:00')
windowSize = 2 * 60
endTime = startTime + windowSize

harpyId = 106
bizhawkOffset = 4

for x in range(startTime, endTime):
    b, s = run(x + bizhawkOffset)
    if b and b.battle_id == harpyId:
        print(toTimeFormat(x))
```

The `run()` function defined above the main body simulates a single IGT. It executes the `s.walk()` function up to 10,000 times, each representing one frame of movement.

```python
def run(igt: int):
    s = State(igt)

    try:
        for _ in range(10000):
            s.walk(REGION_IDS.Gold_Saucer, GROUND_TYPE_IDS.Gold_Saucer_Desert, lr=False)

        return None, s

    except Battle as b:
        return b, s
```

If `s.walk()` finds an encounter on that frame, it raises a `Battle` exception representing the battle that was found. The `run()` function then returns that battle to the main body which then checks the `battle_id` to see if it's a harpy. If `run()` does not find an encounter for that IGT, `None` is returned. If you're looking for IGTs with no encounters, your main body would check for `None` instead of checking the `battle_id`.

```python
for igt in range(startTime, endTime):
    b, s = run(igt)
    if not b:
        print(toTimeFormat(x))
```

See other example scripts for more complex manipulations. The harpy script loops over potential IGTS, but some scripts may nest loops for buffered vs. non-buffered movement while loading the world map, using menus to advance RNG, or adding single frame inputs to manipulate fractions and/or RNG.

[comment]: # (TODO: Add "World Map Battle Mechanics" section)
