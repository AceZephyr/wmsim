from state import State, Battle
import copy

MAXMENUS = 5


def nextStep(s: State, menus: int):

    for _ in range(menus):
        s.rng.rand()

    try:
        s.walk(0xB, 0xA, True, chocotracks=False)
    except Battle:
        return False

    try:
        while s.frac != 0x10:
            s.walk(0xB, 0xA, True, chocotracks=False)
    except Battle:
        raise Exception("wtf")

    if s.walkframes > 900:
        return [menus]

    for m in range(MAXMENUS + 1):
        n = nextStep(copy.deepcopy(s), m)
        if n is not False and n is not None:
            n.append(menus)
            return n


s = State(3 * 60 * 60 + 35 * 60 + 22)

# uncomment this if you hold left during fadein
for _ in range(13):
    s.rng.rand()

n = nextStep(copy.deepcopy(s), 0)
if n is not None:
    n.reverse()
    print(n)
    a = 0
    for x in n:
        if x != 0:
            print(a, "|", x)
        a += 1
    print("total:", sum(n))
else:
    print("oof")
