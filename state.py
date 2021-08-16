from constants import *
from wmrng import WorldMapRNG as RNG


class Battle(Exception):
    def __init__(self, battle_id, local2, local9):
        self.battle_id = battle_id
        self.local2 = local2
        self.local9 = local9


class EncTable:

    def __init__(self, b):
        self.encrate = b[0]
        self.standard = [b[x] for x in range(1, 7)]
        self.special = [b[x] for x in range(7, 11)]
        self.alt = [b[x] for x in range(11, 15)]


class State:
    def __init__(self, igt: int):
        self.rng = RNG(igt)
        # print(" ".join([hex(x)[2:].upper() for x in self.rng.rng]))
        self.frac = -0x8c
        self.danger = 0
        self.lureval = 0x10
        self.chocoval = 0x0
        self.preemptval = 0x10
        self.lastenc = -1

        self.walkframes = 0

    def vehicle_frac_reset(self):
        self.frac = -0x1e

    def preempt_function(self):
        tmp = self.preemptval & 0x7F
        return tmp * (int(tmp > 0x10) + 1)

    def preempt_128(self):
        return int((self.preemptval & 0x80) != 0)

    def enc_check(self, enctable: EncTable):
        enc = -1
        local2 = 0
        local9 = 0  # 1 if yuffie
        self.danger += (self.lureval << 0xA) // ((enctable.encrate >> 8) & 0xFF)
        if self.rng.rand() < (self.danger >> 8) and (enctable.encrate & 1):  # we got a battle
            if self.rng.rand() and False:  # yuffie check, assume it fails for now
                pass
            else:
                if self.chocoval > 0:
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
                                else:
                                    raise Exception("oh no")

                local2 = self.rng.rand() < self.preempt_function()
                if not local2:  # special encs check
                    if enc < 0:
                        tmp = self.rng.rand() << (self.preempt_128() + 8)
                        threshold = enctable.special[0]
                        if threshold > tmp:
                            enc = enctable.special[0] & 0x3FF
                        else:
                            threshold += enctable.special[1]
                            if threshold > tmp:
                                enc = enctable.special[1] & 0x3FF

                    if enc < 0:  # still need to figure out the other condition here
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
            raise Battle(enc, local2, local9)

    def walk(self, region: int, ground_type: int, lr: bool):
        if lr:
            self.rng.rand()
        if ground_type == 0x10:
            ground_type = 0
        if ground_type == 0x18:
            ground_type = 8
        if ground_type in GROUND_TYPES[region]:
            if self.frac >= 0x10:
                self.frac = 0
                self.enc_check(EncTable(ENCOUNTER_DATA[region][GROUND_TYPES[region].index(ground_type)]))
            else:
                self.frac += 1
        self.walkframes += 1
