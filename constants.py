GROUND_TYPES = [
    [0, 9, 0, 17],  #0:  Midgar
    [0, 0, 0, 17],  #1:  Grasslands
    [0, 9, 1, 17],  #2:  Junon
    [0, 20, 0, 17], #3:  Corel
    [0, 9, 8, 17],  #4:  Gold Saucer
    [0, 0, 25, 17], #5:  Gongaga
    [0, 9, 19, 17], #6:  Cosmo
    [0, 0, 1, 17],  #7:  Nibel
    [0, 0, 1, 17],  #8:  Rocket Launch Pad
    [0, 9, 14, 17], #9:  Wutai
    [0, 9, 25, 17], #10: Woodlands
    [0, 10, 9, 17], #11: Icicle
    [0, 9, 25, 17], #12: Mideel
    [0, 0, 8, 11],  #13: North Corel
    [0, 0, 8, 0],   #14: Cactus Island
    [0, 0, 1, 0]    #15: Goblin Island
]

# See https://ff7speedruns.com/index.php/World_Map_Encounter_Mechanics
# This can be used as an index for GROUND_TYPES
class REGION_IDS():
    Midgar = 0
    Grasslands = 1
    Junon = 2
    Corel = 3
    Gold_Saucer = 4
    Gongaga = 5
    Cosmo = 6
    Nibel = 7
    Rocket_Launch_Pad = 8
    Wutai = 9
    Woodlands = 10
    Icicle = 11
    Mideel = 12
    North_Corel = 13
    Cactus_Island = 14
    Goblin_Island = 15
    Round_Island = 15 # Same as Goblin_Island

# See https://ff7speedruns.com/index.php/World_Map_Encounter_Mechanics
class GROUND_TYPE_IDS():
    Grass = 0                         # Most things can go here.
    Forest = 1                        # No landing here, but anything else goes.
    Mountain = 2                      # Chocobos and flying machines only.
    Sea = 3                           # Deep water, only gold chocobo and submarine can go here.
    River_Crossing = 4                # Buggy, tiny bronco and water-capable chocobos.
    River = 5                         # Tiny bronco and chocobos.
    Water = 6                         # Shallow water, same as above.
    Swamp = 7                         # Midgar zolom can only move in swamp areas.
    Desert = 8                        # No landing.
    Wasteland = 9                     # Found around Midgar, Wutai and misc other. No landing.
    Snow = 10                         # Leaves footprints, no landing.
    Riverside = 11                    # Beach-like area where river and land meet.
    Cliff = 12                        # Sharp drop, usually where the player can be on either side.
    Corel_Bridge = 13                 # Tiny bridge over the waterfall from Costa del Sol to Corel.
    Wutai_Bridge = 14                 # Rickety rope bridges south of Wutai.
    Unused_1 = 15                     # Doesn't seem to be used anywhere in the original data.
    Hill_Side = 16                    # This is the tiny walkable part at the foot of a mountain.
    Beach = 17                        # Where land and shallow water meets.
    Sub_Pen = 18                      # Only place where you can enter/exit the submarine.
    Canyon = 19                       # The ground in cosmo canyon has this type, walkability seems to be the same as wasteland.
    Mountain_Pass = 20                # The small path through the mountains connecting Costa del Sol and Corel.
    Unknown = 21                      # Present around bridges, may have some special meaning.
    Waterfall = 22                    # River type where the tiny bronco can't go.
    Unused_2 = 23                     # Doesn't seem to be used anywhere in the original data.
    Gold_Saucer_Desert = 24           # Special desert type for the golden saucer.
    Jungle = 25                       # Walkability same as forest, used in southern parts of the map.
    Sea_2 = 26                        # Special type of deep water, only used in one small spot next to HP-MP cave, possibly related to the underwater map/submarine.
    Northern_Cave = 27                # Inside part of the crater, where you can land the highwind.
    Gold_Saucer_Desert_Border = 28    # Narrow strip of land surrounding the golden saucer desert. Probably related to the "quicksand" script.
    Bridgehead = 29                   # Small area at both ends of every bridge. May have some special meaning.
    Back_Entrance = 30                # Special type that can be set unwalkable from the script.
    Unused_3: 31                      # Doesn't seem to be used anywhere in the original data.

ENCOUNTER_DATA = [[[8193, 16422, 16423, 16424, 16425, 0, 0, 2090, 2090, 0, 4139, 0, 0, 0, 0, 0],
                   [5121, 16416, 16417, 16418, 16420, 0, 0, 4131, 4131, 10277, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [16385, 22572, 21549, 21550, 0, 0, 0, 0, 0, 0, 8239, 0, 0, 0, 0, 0]],
                  [[8193, 13360, 13361, 13362, 13363, 12340, 0, 2101, 2102, 0, 4151, 24632, 24633, 24636, 24637, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [16385, 16442, 16443, 16446, 16447, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                  [[8193, 16448, 16449, 16450, 16451, 0, 0, 4164, 4165, 0, 0, 16462, 16463, 16464, 16465, 0],
                   [5121, 22598, 21575, 21576, 0, 0, 0, 4169, 4169, 0, 0, 0, 0, 0, 0, 0],
                   [3073, 16458, 16458, 16459, 16459, 0, 0, 4172, 4172, 0, 0, 0, 0, 0, 0, 0],
                   [16385, 22605, 21586, 21587, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                  [[8193, 22612, 21588, 21588, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [8193, 22614, 21592, 21593, 0, 0, 0, 4186, 4186, 16475, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [16385, 16469, 16476, 16477, 16478, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                  [[8193, 22624, 21601, 21604, 0, 0, 0, 4197, 4197, 0, 0, 5218, 5219, 11368, 11369, 0],
                   [5121, 32870, 32870, 0, 0, 0, 0, 0, 0, 10343, 0, 0, 0, 0, 0, 0],
                   [8193, 32874, 32875, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [16385, 16469, 16476, 16477, 16478, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                  [[8193, 22636, 21613, 21614, 0, 0, 0, 2159, 2159, 0, 4208, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [5121, 22641, 21618, 21619, 0, 0, 0, 0, 0, 0, 8308, 0, 0, 0, 0, 0],
                   [16385, 16469, 16476, 16477, 16478, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                  [[8193, 22636, 21613, 21614, 0, 0, 0, 2159, 2159, 0, 4208, 0, 0, 0, 0, 0],
                   [5121, 22648, 21625, 21626, 0, 0, 0, 4219, 4219, 0, 0, 0, 0, 0, 0, 0],
                   [8193, 11388, 11389, 11390, 11391, 10368, 10369, 2178, 2179, 10372, 4229, 0, 0, 0, 0, 0],
                   [16385, 22662, 21639, 21640, 0, 0, 0, 0, 0, 0, 8329, 0, 0, 0, 0, 0]],
                  [[8193, 22668, 21645, 21646, 0, 0, 0, 4239, 4239, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [3073, 22672, 21649, 21650, 0, 0, 0, 0, 0, 0, 8339, 0, 0, 0, 0, 0],
                   [16385, 22662, 21639, 21640, 0, 0, 0, 0, 0, 0, 8329, 0, 0, 0, 0, 0]],
                  [[8193, 22676, 21653, 21654, 0, 0, 0, 0, 0, 0, 8343, 5272, 5273, 11420, 11421, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [3073, 22682, 21659, 21662, 0, 0, 0, 4255, 4255, 0, 0, 0, 0, 0, 0, 0],
                   [16385, 22662, 21639, 21640, 0, 0, 0, 0, 0, 0, 8329, 0, 0, 0, 0, 0]],
                  [[16385, 16544, 16545, 16548, 16549, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [16385, 16552, 16553, 16554, 16555, 0, 0, 2220, 2221, 10414, 4271, 8354, 8355, 8358, 8359, 0],
                   [5121, 32944, 32945, 0, 0, 0, 0, 0, 0, 0, 8370, 0, 0, 0, 0, 0],
                   [24577, 32947, 32947, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                  [[8193, 22708, 21685, 21686, 0, 0, 0, 4279, 4279, 0, 0, 0, 0, 0, 0, 0],
                   [8193, 22712, 21689, 21690, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [3073, 22716, 21693, 21694, 0, 0, 0, 0, 0, 0, 8383, 0, 0, 0, 0, 0],
                   [24577, 32955, 32955, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                  [[8193, 22720, 21697, 21698, 0, 0, 0, 4291, 4292, 0, 0, 0, 0, 0, 0, 0],
                   [8193, 13509, 13510, 13511, 13512, 12489, 0, 2252, 2252, 0, 4301, 3274, 3275, 13518, 13519, 0],
                   [24577, 22736, 21713, 21714, 0, 0, 0, 0, 0, 10451, 0, 0, 0, 0, 0, 0],
                   [24577, 32955, 32955, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                  [[8193, 16596, 16597, 16600, 16601, 0, 0, 0, 0, 0, 0, 7382, 7383, 9434, 9435, 0],
                   [5121, 22748, 21725, 21726, 0, 0, 0, 4319, 4319, 0, 0, 0, 0, 0, 0, 0],
                   [3073, 22752, 21729, 21730, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [24577, 32995, 32995, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                  [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [24577, 20712, 20713, 16612, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                  [[16385, 22757, 21734, 21735, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],#
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [24577, 41188, 24804, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
                  [[16385, 22757, 21734, 21735, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [16385, 22762, 21739, 21740, 0, 0, 0, 2285, 2285, 10478, 4335, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]]
