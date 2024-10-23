import string
import tracemalloc
from memory_profiler import profile

suit_to_num = {"C": 0, "D": 1, "H": 2, "S": 3, "NT": 4}
num_to_suit = ["C", "D", "H", "S", "NT"]


class bid:
    def __init__(self, str):
        if str == "X":
            self.suit = ""
            self.level = 0
            self.call = "X"
        elif str == "XX":
            self.suit = ""
            self.level = 0
            self.call = "XX"
        elif str == "P":
            self.suit = ""
            self.level = 0
            self.call = "P"
        elif len(str) == 3:
            self.suit = 4
            self.level = int(str[0])
            self.call = "B"
        else:
            self.suit = suit_to_num[str[1]]
            self.level = int(str[0])
            self.call = "B"

    def __repr__(self):
        if self.call == "B":
            return str(self.level) + num_to_suit[self.suit]
        else:
            return self.call


def str_to_sequence(str):
    bids_str = str.split(" ")
    bids = []
    for b in bids_str:
        bids.append(bid(b))
    return bids


possible_bids = []
for level in ["1", "2", "3", "4", "5", "6", "7"]:
    for suit in ["C", "D", "H", "S", "NT"]:
        possible_bids.append(bid(level + suit))


def valid_bids(sequence):
    last_bid = sequence[-1]
    v_bids = []

    highest_call = bid("1C")
    for i in range(len(sequence) - 1, -1, 1):
        if sequence[i].call == "B":
            highest_call = sequence[i]
            break

    if len(sequence) > 2:
        if sequence[-1].call == "P" and sequence[-2].call == "P":
            if sequence[-3].call == "B":
                v_bids.append(bid("X"))
            if sequence[-3].call == "X":
                v_bids.append(bid("XX"))

    if sequence[-1].call == "B":
        v_bids.append(bid("X"))
    if sequence[-1].call == "X":
        v_bids.append(bid("XX"))

    v_bids = v_bids + possible_bids[highest_call.suit + (highest_call.level - 1) * 5 :]

    return v_bids


class description:
    def __init__(self, shapes, highs, keycards, control_points, controls, forced):
        self.shapes = (
            shapes  # [(5,4,3,1),(5,4,2,2) ... (13,0,0,0)] is 1 spade opener shape
        )
        self.highs = highs  # []
        self.keycards = keycards  # Responses to a blackwood esc asking bid
        self.control_points = control_points  # A-2, K-1
        self.controls = (
            controls  # [1,0,2,0] First round control in spades, second in diamonds
        )
        self.forced = forced  # true if bid is forced (2N lebenshol forces 3C, Transfers to the minors)


def bidding_key(shape, highs):
    return (((shape[0] * 13 + shape[1]) * 13 + shape[2]) * 13 + shape[3]) * 40 + highs


def bidding_decode(key):
    highs = key % 41
    key = (key - highs) / 41
    shape = [0, 0, 0, 0]
    shape[3] = key % 13
    key = (key - shape[3]) / 13
    shape[2] = key % 13
    key = (key - shape[2]) / 13
    shape[1] = key % 13
    key = (key - shape[1]) / 13
    shape[0] = key
    return shape, highs


class bidding_table:
    def __init__(self, highs_range, possible_shapes):
        self.possible_shapes = possible_shapes
        self.highs_range = highs_range
        self.table = dict()

        for i in self.possible_shapes:
            for j in range(self.highs_range[0], self.highs_range[1] + 1, 1):
                key = (((i[0] * 13 + i[1]) * 13 + i[2]) * 13 + i[3]) * 41 + j
                self.table[key] = "2D"


def generate_shapes(spade_range, heart_range, diamond_range, club_range):
    shapes = []
    for s in range(spade_range[0], spade_range[1] + 1, 1):
        for h in range(s + heart_range[0], min(s + heart_range[1] + 1, 14), 1):
            for d in range(h + diamond_range[0], min(h + diamond_range[1] + 1, 14), 1):
                c = 13 - d
                if c > club_range[1] or c < club_range[0]:
                    continue
                shapes.append([s, h - s, d - h, c])

    print(len(shapes))
    return shapes


# Use a bidding table for some bids, and use description for others

# Opening and responding bids should use the bid table, keycard should not.

# Bid table is a table where x axis is points and y axis is possible shapes.
# Each entry is a list of possible valid bids.
# This will help in differentiating certain shapes (5 spades and 5 hearts opens 1H or 1S for example)


class convention:
    def __init__(self, bidding_sequence):
        self.bidding_sequence = bidding_sequence

        self.responses = valid_bids(bidding_sequence)

        self.description = []

    def undescribed_hands(self):
        return

    def add_description(self):

        input("")
        return


def describe_hands(bids, dealer, NS_System, EW_System):
    return


# starting the monitoring
tracemalloc.start()

# function call

test = bidding_table([0, 40], generate_shapes((0, 13), (0, 13), (0, 13), (0, 13)))


# displaying the memory
print(tracemalloc.get_traced_memory())

# stopping the library
tracemalloc.stop()
print()
