# wmsim

wmsim is a World Map RNG simulation library for Final Fantasy VII.
It can be used to generate lists of IGTs for performing manipulations used in speedruns, for example.

# Usage

wmsim is written in Python 3 but the library itself has no other dependencies.
Most of the examples have a dependency on the `tabulate` package which can be installed with `pip3 install tabulate`.

Primarily, you use wmsim by creating `State` objects and using their `walk()` method to simulate one frame
of world map RNG at a time. Eventually, a call to `walk` will throw a `Battle`, which is a kind of exception,
which can be caught to determine when a battle takes place and what battle it is.

```python
from constants import *
from state import State, Battle

# Seed the world map at 3:14:15
s = State(3 * HOURS + 14 * MINUTES + 15, zolombox_init=True)
s.chocoval = 8

try:
    for _ in range(10000):
        s.walk(Region.Grasslands, Ground.Grass, True, chocotracks=True, zolombox=True)
except Battle as b:
    print(b.battle_id)
```

# Known Limitations and Quirks

- wmsim does not simulate the time it takes for the game to load after transitioning from a field or battle.
All IGT times provided to wmsim are the times at which the world map is seeded, and are directly used without
any conversion or compensation made for the potential time it could have taken to load into the world map.
- wmsim does not simulate the position or exact behavior of the Midgar Zolom beyond the RNG calls it makes
while moving passively. This is sufficient to simulate its effect on RNG if the player is within the zolom box
but not on Swampland (type 7) ground, which is when the Zolom will actively hunt the player and its behavior
changes. This means that wmsim cannot be used to simulate manipulating the Zolom while passing through the marsh.
- The behavior of the Zolom while opening the menu in the Zolom Box must be manually emulated
(see `examples/midgar_choco_0enc.py`)
- It is untested if wmsim properly simulates the North Corel Area encounter table, which has a bug where 1/8 of 
its encounter table is undefined and does not generate a battle.
- wmsim does not have an automatic mechanism to simulate the RNG calls made by 
Ultimate Weapon, Emerald Weapon, or Ruby Weapon, which call RNG in their behavioral scripts.
(Emerald and Ruby are easy to emulate, as they only perform a single call on spawn)
- If not running in PyCharm, the example scripts may need to be moved so they can properly find their imports.