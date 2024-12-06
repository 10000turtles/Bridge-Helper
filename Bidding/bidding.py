import string
import tracemalloc
from memory_profiler import profile
import pickle
from ast import literal_eval
import itertools
from itertools import zip_longest
import time
from deck_of_cards import deck_of_cards
import math
import hand_gen

suit_to_num = {"C": 0, "D": 1, "H": 2, "S": 3, "NT": 4}
num_to_suit = ["C", "D", "H", "S", "NT"]

str_to_card = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


def sort_suit(suit):
    sorted = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    if len(suit) > 0:
        indx = [sorted.index(i) for i in suit]
        indx.sort()
        suit = "".join([sorted[i] for i in indx])
    return suit


class hand:
    def __init__(self, s):
        self.spades = []
        self.hearts = []
        self.diamonds = []
        self.clubs = []
        self.string = s
        self.suits = [self.spades, self.hearts, self.diamonds, self.clubs]
        counter = 0
        for suit in s.split(":"):
            for c in list(suit):
                self.suits[counter].append(str_to_card[c])
            counter = counter + 1

        self.points = 0
        self.shape = [0, 0, 0, 0]
        counter = 0
        for s in self.suits:
            for c in s:
                if c > 10:
                    self.points = self.points + c - 10
                self.shape[counter] = self.shape[counter] + 1
            counter = counter + 1


class bid:
    def __init__(self, s):
        if s == "X":
            self.suit = ""
            self.level = 0
            self.call = "X"
            self.string = "X"
        elif s == "XX":
            self.suit = ""
            self.level = 0
            self.call = "XX"
            self.string = "XX"
        elif s == "P":
            self.suit = ""
            self.level = 0
            self.call = "P"
            self.string = "P"
        elif len(s) == 3:
            self.suit = 4
            self.level = int(s[0])
            self.call = "B"
            self.string = str(self.level) + num_to_suit[self.suit]
        else:
            self.suit = suit_to_num[s[1]]
            self.level = int(s[0])
            self.call = "B"
            self.string = str(self.level) + num_to_suit[self.suit]

    def __repr__(self):
        if self.call == "B":
            return self.string
        else:
            return self.call

    def __eq__(self, other):
        return self.string == other.string


def str_to_sequence(s):
    bids_str = ("".join(s.split())).split(",")
    if bids_str[0] == "":
        return []
    bids = []
    for b in bids_str:
        bids.append(bid(b))
    return bids


possible_bids = []
for level in ["1", "2", "3", "4", "5", "6", "7"]:
    for suit in ["C", "D", "H", "S", "NT"]:
        possible_bids.append(bid(level + suit))


def valid_bids(sequence):
    v_bids = []

    if len(sequence) > 3:
        if sequence[-1].call == "P" and (
            sequence[-2].call == "P" and sequence[-3].call == "P"
        ):
            return v_bids

    highest_call = bid("1C")

    for i in range(len(sequence) - 1, -1, -1):
        if sequence[i].call == "B":
            highest_call = sequence[i]
            break

    if len(sequence) > 2:
        if sequence[-1].call == "P" and sequence[-2].call == "P":
            if sequence[-3].call == "B":
                v_bids.append(bid("X"))
            if sequence[-3].call == "X":
                v_bids.append(bid("XX"))
    if len(sequence) > 1:
        if sequence[-1].call == "B":
            v_bids.append(bid("X"))
        if sequence[-1].call == "X":
            v_bids.append(bid("XX"))

    v_bids = v_bids + possible_bids[highest_call.suit + (highest_call.level - 1) * 5 :]

    return v_bids


class description:
    def __init__(self, shapes, keycards, control_points, controls, forced):
        self.shapes = shapes  # [[[5,5],[0,5],[0,13],[0,13],[11,15]],[[6,13],[0,13],[0,13],[0,13],[10,15]]] 1 spade opener
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


def generate_shapes(spade_range, heart_range, diamond_range, club_range):
    shapes = []
    for s in range(spade_range[0], spade_range[1] + 1, 1):
        for h in range(s + heart_range[0], min(s + heart_range[1] + 1, 14), 1):
            for d in range(h + diamond_range[0], min(h + diamond_range[1] + 1, 14), 1):
                c = 13 - d
                if c > club_range[1] or c < club_range[0]:
                    continue
                shapes.append([s, h - s, d - h, c])

    return shapes


# Use a bidding table for some bids, and use description for others

# Opening and responding bids should use the bid table, keycard should not.

# Bid table is a table where x axis is points and y axis is possible shapes.
# Each entry is a list of possible valid bids.
# This will help in differentiating certain shapes (5 spades and 5 hearts opens 1H or 1S for example)


class convention:
    def __init__(self, bidding_sequence):
        self.bidding_sequence = str_to_sequence(bidding_sequence)

        self.undefined_responses = valid_bids(self.bidding_sequence)

        self.bids = []
        self.descriptions = []

    def save_object(self, filename):
        with open(filename, "wb") as outp:
            pickle.dump(self.bidding_sequence, outp, pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.responses, outp, pickle.HIGHEST_PROTOCOL)
            pickle.dump(self.descriptions, outp, pickle.HIGHEST_PROTOCOL)

    def load_object(self, filename):
        with open(filename, "rb") as input:  # Overwrites any existing file.
            self.bidding_sequence = pickle.load(input)
            self.responses = pickle.load(input)
            self.descriptions = pickle.load(input)

    def add_description(self, b, shape):
        self.bids.append(b)
        self.descriptions.append(description(shape, "", "", "", ""))

    def what_to_bid(self, han: hand):

        possible_bids = []

        for b, desc in zip(self.bids, self.descriptions):
            for shape in desc.shapes:
                count = 0
                is_shape = True
                is_strength = True
                for range in shape[0:4]:
                    if han.shape[count] > range[1] or han.shape[count] < range[0]:
                        is_shape = False
                        break
                    count = count + 1
                if han.points > shape[4][1] or han.points < shape[4][0]:
                    is_strength = False

                if is_shape and is_strength:
                    possible_bids.append(b)
                    break
        if len(possible_bids) == 0:
            return ["P"]

        return possible_bids


def describe_hands(bids, dealer, NS_System, EW_System):
    return


def grouper(n, iterable, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def random_hand():
    deck = deck_of_cards.DeckOfCards()

    names = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
    s = ""
    h = ""
    d = ""
    c = ""

    for i in range(0, 13, 1):
        card = deck.give_random_card()
        if card.suit == 0:
            s = s + names[card.rank - 1]
        if card.suit == 1:
            h = h + names[card.rank - 1]
        if card.suit == 2:
            d = d + names[card.rank - 1]
        if card.suit == 3:
            c = c + names[card.rank - 1]

    s = sort_suit(s)
    h = sort_suit(h)
    d = sort_suit(d)
    c = sort_suit(c)

    return s + ":" + h + ":" + d + ":" + c


class system:
    def __init__(self):
        self.conventions = []

    def bulk_add_convention(self, filename):
        with open(filename, "r") as input:
            s = input.read()
            inputs = ("".join(s.split())).split(":")

            for seq, b, desc in list(grouper(3, inputs)):
                try:
                    ind = [i.bidding_sequence for i in self.conventions].index(
                        str_to_sequence(seq)
                    )
                    self.conventions[ind].add_description(b, literal_eval(desc))
                except:
                    self.conventions.append(convention(seq))
                    self.conventions[-1].add_description(b, literal_eval(desc))

    def what_to_bid(self, hand, sequence):
        for conv in self.conventions:
            if conv.bidding_sequence == sequence:
                return conv.what_to_bid(hand)
        return "P"


def bid_a_hand(n_s_system: system, e_w_system: system, hands, dealer: int):

    bidding_sequence = []
    val_bid = valid_bids(bidding_sequence)

    person_to_bid = dealer

    while len(val_bid) > 0:
        next_bid = ""
        if person_to_bid == 0 or person_to_bid == 2:
            next_bid = n_s_system.what_to_bid(hands[person_to_bid], bidding_sequence)
        else:
            next_bid = e_w_system.what_to_bid(hands[person_to_bid], bidding_sequence)

        bidding_sequence.append(bid(next_bid[0]))

        person_to_bid = (person_to_bid + 1) % 4
        val_bid = valid_bids(bidding_sequence)
    for i in hands:
        print(i.string)
    print(bidding_sequence)


sayc = system()
sayc.bulk_add_convention("SAYC.txt")

hands = hand_gen.hand_gen(
    [[2, 4], [2, 4], [2, 6], [2, 6], [15, 17]],
    [[0, 13], [0, 13], [0, 13], [0, 13], [0, 30]],
    [[0, 13], [0, 13], [0, 13], [0, 13], [0, 30]],
    [[0, 13], [0, 13], [0, 13], [0, 13], [0, 30]],
)

hands = [hand(i) for i in hands]

bid_a_hand(sayc, sayc, hands, 0)


# itr = 1000000

# for i in range(0, itr, 1):
#     if i % (math.floor(itr / 100)) == 0:
#         print(str(i / itr * 100) + "%")
#     h = hand(random_hand())
#     bids = sayc.what_to_bid(h, str_to_sequence("1NT, P"))

#     if len(bids) != 1:
#         print(h.string)
#         print(h.shape)
#         print(h.points)
#         print(bids)
