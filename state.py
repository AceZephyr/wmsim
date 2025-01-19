from constants import *
from wmrng import WorldMapRNG as RNG


class Battle(Exception):
    """
    Describes a random battle that occurs on the World Map. Thrown by State.walk.

    :var battle_id: Battle ID. If this is a Mystery Ninja battle, this will be -1.
    :var preempt: Boolean. If true, this battle is flagged as preemptive. Note that a battle with a non-preemptable flag may still be flagged as preemptive, in which case the battle will not actually be preemptive.
    :var chocobo: Boolean. If true, this is a battle against a Chocobo that can be caught.
    :var yuffie: Boolean. If true, this is a battle against the Mystery Ninja.
    """

    def __init__(self, battle_id, preempt, yuffie=False, chocobo=False):
        self.battle_id = battle_id
        self.preempt = preempt
        self.yuffie = yuffie
        self.chocobo = chocobo


class EncTable:

    def __init__(self, b):
        self.encrate = b[0]
        self.standard = [b[x] for x in range(1, 7)]
        self.special = [b[x] for x in range(7, 11)]
        self.alt = [b[x] for x in range(11, 15)]


class State:
    """
    Describes the state of the world map and all data needed to maintain that state. Use walk() to perform simulations.
    """

    def __init__(self, igt: int, zolombox_init: bool = False):
        """
        State constructor. Note that the IGt given is the IGT at which the world map is seeded, not the IGT at which an action is performed to exit to the world map. Depending on game version and circumstance, there is a delay until when the world map is seeded. This is often 3 seconds on the PSX version, but varies and should be tested in individual circumstances.

        :param igt: The world map's seeding IGT
        :param zolombox_init: Boolean (default=False): This should be True if the player spawns within the Zolom Box when entering the world map.
        """
        self.rng = RNG(igt)
        self.frac = -0x8c
        self.danger = 0
        self.lureval = 0x10
        self.chocoval = 0x0
        self.preemptval = 0x10
        self.lastenc = -1

        self.walkframes = 0

        self.zolom_timer = 0

        self.encounter_checks = 0

        self.movement_frames = 0

        if zolombox_init:
            self.zolom_tick()

    def vehicle_frac_reset(self):
        self.frac = -0x1e

    def lure_function(self):
        return self.lureval * (int(self.lureval > 0x10) + 1)

    def preempt_function(self):
        tmp = self.preemptval & 0x7F
        return tmp * (int(tmp > 0x10) + 1)

    def preempt_128(self):
        return int((self.preemptval & 0x80) != 0)

    def enc_check(self, enctable: EncTable, chocotracks: bool = False, more_than_one_party_member: bool = True,
                  yuffie_chance: int = 0):
        self.encounter_checks += 1
        enc = -1
        is_preempt = 0
        is_chocobo_battle = False
        self.danger += (self.lure_function() << 0xA) // ((enctable.encrate >> 8) & 0xFF)
        if self.rng.rand() < (self.danger >> 8) and (enctable.encrate & 1):  # we got a battle
            yuffie_rand = self.rng.rand()
            if yuffie_rand < yuffie_chance:
                raise Battle(battle_id=-1, preempt=False, yuffie=True, chocobo=False)
            else:
                if self.chocoval > 0 and chocotracks:
                    tmp = (self.rng.rand() << 0xC) / self.chocoval
                    threshold = enctable.alt[0]
                    if threshold > tmp:
                        enc = enctable.alt[0] & 0x3FF
                    else:
                        threshold += enctable.alt[1]
                        if threshold > tmp:
                            enc = enctable.alt[1] & 0x3FF
                        else:
                            threshold += enctable.alt[2]
                            if threshold > tmp:
                                enc = enctable.alt[2] & 0x3FF
                            else:
                                threshold += enctable.alt[3]
                                if threshold > tmp:
                                    enc = enctable.alt[3] & 0x3FF
                    if enc >= 0:
                        is_chocobo_battle = True

                is_preempt = self.rng.rand() < self.preempt_function()
                if not is_preempt:  # special encs check
                    if enc < 0:
                        tmp = self.rng.rand() << (self.preempt_128() + 8)
                        threshold = enctable.special[0]
                        if threshold > tmp:
                            enc = enctable.special[0] & 0x3FF
                        else:
                            threshold += enctable.special[1]
                            if threshold > tmp:
                                enc = enctable.special[1] & 0x3FF

                    if more_than_one_party_member and enc < 0:
                        tmp = self.rng.rand() << 8
                        threshold = enctable.special[2]
                        if threshold > tmp:
                            enc = enctable.special[2] & 0x3FF

                    if enc < 0:
                        tmp = self.rng.rand() << (self.preempt_128() + 8)
                        threshold = enctable.special[3]
                        if threshold > tmp:
                            enc = enctable.special[3] & 0x3FF

                if enc < 0:
                    checks = 0
                    while True:
                        tmp = self.rng.rand() << 8
                        threshold = enctable.standard[0]
                        if threshold > tmp:
                            enc = enctable.standard[0] & 0x3FF
                        else:
                            threshold += enctable.standard[1]
                            if threshold > tmp:
                                enc = enctable.standard[1] & 0x3FF
                            else:
                                threshold += enctable.standard[2]
                                if threshold > tmp:
                                    enc = enctable.standard[2] & 0x3FF
                                else:
                                    threshold += enctable.standard[3]
                                    if threshold > tmp:
                                        enc = enctable.standard[3] & 0x3FF
                                    else:
                                        threshold += enctable.standard[4]
                                        if threshold > tmp:
                                            enc = enctable.standard[4] & 0x3FF
                                        else:
                                            threshold += enctable.standard[5]
                                            if threshold > tmp:
                                                enc = enctable.standard[5] & 0x3FF
                                            else:
                                                raise Exception("oh no")
                        if checks != 0 or enc != self.lastenc:
                            break
                        checks += 1
        if enc != -1:
            raise Battle(enc, preempt=is_preempt, yuffie=False, chocobo=is_chocobo_battle)

    def zolom_tick(self):
        if self.zolom_timer <= 0:
            self.zolom_timer = (self.rng.rand() + 0x40) >> 2
            self.rng.rand()
        else:
            self.zolom_timer -= 1

    def walk(self, region: int, ground_type: int, lr: bool, movement: bool = True, zolombox: bool = False,
             chocotracks: bool = False, more_than_one_party_member: bool = True, yuffie_chance: int = 0):
        """
        Performs one frame of world map simulation, simulating left/right incrementation, passive zolom behavior, and
        encounter logic.

        :param region: Integer (required). Region ID. See constants.Region
        :param ground_type: Integer (required). Ground type ID. See constants.Ground
        :param lr: Boolean (required). If true, any of Left, Right, L1, or R1 are simulated as being pressed on this frame, and the corresponding RNG call happens.
        :param movement: Boolean (default=True). If true, Fractions increment on this frame as a result of the player moving. If false, Fractions do not increment, either because no movement occurs, that movement is menu-buffered, or the current ground triangle is not hostile.
        :param zolombox: Boolean (default=False). If true, the player is within the Zolom box and passive Zolom behavior is performed.
        :param chocotracks: Boolean (default=False). If true, the ground the player is standing on is flagged to be able to spawn a Chocobo encounter.
        :param more_than_one_party_member: Boolean. If false, the party consists of exactly one party member. (Usually true)
        :param yuffie_chance: Integer. The chance for the Mystery Ninja to appear should an encounter check happen on this frame of movement (out of 256). See constants.MysteryNinja
        :raise Battle: If a battle occurs, Battle is thrown.
        """
        if lr:
            self.rng.rand()
        if zolombox:
            self.zolom_tick()
        if movement:
            if self.frac >= 0x10:
                self.frac = 0
                if ground_type == 0x10:
                    ground_type = 0
                if ground_type == 0x18:
                    ground_type = 8
                ground_idx = 0
                if ground_type in GROUND_TYPES[region]:
                    ground_idx = GROUND_TYPES[region].index(ground_type)
                self.enc_check(enctable=EncTable(ENCOUNTER_DATA[region][ground_idx]),
                               chocotracks=chocotracks, more_than_one_party_member=more_than_one_party_member,
                               yuffie_chance=yuffie_chance)
            else:
                self.frac += 1
        if movement:
            self.walkframes += 1
