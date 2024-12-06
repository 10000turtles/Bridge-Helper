import string
import tracemalloc
from memory_profiler import profile
import pickle
from ast import literal_eval
import itertools
from itertools import zip_longest
import time
import math
import random


def sort_suit(suit):
    sorted = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

    if len(suit) > 0:
        indx = [sorted.index(i) for i in suit]
        indx.sort()
        suit = "".join([sorted[i] for i in indx])
    return suit


rank_to_str = [
    "",
    "",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "T",
    "J",
    "Q",
    "K",
    "A",
]
suit_to_str = ["S", "H", "D", "C"]
suit_key_abr = {"S": 0, "H": 1, "D": 2, "C": 3}
rank_key_abr = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


class card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    @classmethod
    def from_card(cls, card):
        return cls(suit_key_abr[card[1]], rank_key_abr[card[0]])

    def __str__(self):
        return rank_to_str[self.rank] + suit_to_str[self.suit]


class deck:
    def __init__(self):
        self.cards = []

        for i in range(2, 15, 1):
            for j in range(0, 4, 1):
                self.cards.append(card(j, i))

    def face_cards(self):
        self.cards = [i for i in self.cards if i.rank >= 11]
        random.shuffle(self.cards)

    def spot_cards(self):
        self.cards = [i for i in self.cards if i.rank <= 10]
        random.shuffle(self.cards)


suit_key = {"Spades": 0, "Hearts": 1, "Diamonds": 2, "Clubs": 3}
rank_key = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "Jack": 11,
    "Queen": 12,
    "King": 13,
    "Ace": 14,
}


def points(hand):
    jacks = len([i for i in hand if i.rank == 11])
    queens = len([i for i in hand if i.rank == 12])
    kings = len([i for i in hand if i.rank == 13])
    aces = len([i for i in hand if i.rank == 14])

    return aces * 4 + kings * 3 + queens * 2 + jacks


def does_violate_conditions(hand, description, card, dealing_spot_cards):
    pts = points(hand)

    if len(hand) > 12:
        return True

    if pts + points([card]) > description[4][1]:
        return True

    suit_len = len([i for i in hand if i.suit == card.suit])
    if suit_len + 1 > description[card.suit][1]:
        return True

    return False


def are_requirements_being_achieved(hand, description, card, dealing_spot_cards):

    suit_len = len([i for i in hand if i.suit == card.suit])
    pts = points(hand)
    if dealing_spot_cards:
        if suit_len + 1 <= description[card.suit][0]:
            return True
    else:
        if (pts < description[4][0]) and (pts + points([card]) <= description[4][1]):
            if suit_len + 1 <= description[card.suit][0]:
                return True

    return False


def put_to_string(hand):
    spade_str = ""
    heart_str = ""
    diamond_str = ""
    club_str = ""

    for i in hand:
        if i.suit == 0:
            spade_str = spade_str + rank_to_str[i.rank]

    for i in hand:
        if i.suit == 1:
            heart_str = heart_str + rank_to_str[i.rank]

    for i in hand:
        if i.suit == 2:
            diamond_str = diamond_str + rank_to_str[i.rank]

    for i in hand:
        if i.suit == 3:
            club_str = club_str + rank_to_str[i.rank]

    return (
        sort_suit(spade_str)
        + ":"
        + sort_suit(heart_str)
        + ":"
        + sort_suit(diamond_str)
        + ":"
        + sort_suit(club_str)
    )


def hand_gen(north, east, south, west):

    north_cards = []
    east_cards = []
    south_cards = []
    west_cards = []

    deal = [
        (north_cards, north, 0),
        (east_cards, east, 1),
        (south_cards, south, 2),
        (west_cards, west, 3),
    ]

    face = deck()
    spot = deck()

    face.face_cards()
    spot.spot_cards()

    for card in face.cards:
        random.shuffle(deal)
        # print()
        # print("Details of: " + card.__str__())

        card_delt = False

        for pos in deal:

            if are_requirements_being_achieved(pos[0], pos[1], card, False):
                pos[0].append(card)
                card_delt = True

                # print("Hand " + str(pos[2]) + " accepted card: " + card.__str__())
                break
            # print(
            #     "Hand "
            #     + str(pos[2])
            #     + " requirements not being ach by: "
            #     + card.__str__()
            # )
        if card_delt:
            continue
        for pos in deal:
            if not does_violate_conditions(pos[0], pos[1], card, False):
                pos[0].append(card)
                card_delt = True
                # print("Hand " + str(pos[2]) + " accepted card: " + card.__str__())
                break

            # print("Hand " + str(pos[2]) + " is violated by: " + card.__str__())
        if card_delt:
            continue
        west_cards.append(card)

    for card in spot.cards:
        random.shuffle(deal)

        # print()
        # print("Details of: " + card.__str__())

        card_delt = False

        for pos in deal:

            if are_requirements_being_achieved(pos[0], pos[1], card, True):
                pos[0].append(card)
                card_delt = True

                # print("Hand " + str(pos[2]) + " accepted card: " + card.__str__())
                break
            # print(
            #     "Hand "
            #     + str(pos[2])
            #     + " requirements not being ach by: "
            #     + card.__str__()
            # )
        if card_delt:
            continue
        for pos in deal:
            if not does_violate_conditions(pos[0], pos[1], card, True):
                pos[0].append(card)
                card_delt = True
                # print("Hand " + str(pos[2]) + " accepted card: " + card.__str__())
                break

            # print("Hand " + str(pos[2]) + " is violated by: " + card.__str__())
        if card_delt:
            continue
        west_cards.append(card)

    deal = sorted(deal, key=lambda x: x[2])

    return [
        put_to_string(deal[0][0]),
        put_to_string(deal[1][0]),
        put_to_string(deal[2][0]),
        put_to_string(deal[3][0]),
    ]


# sayc = system()
# sayc.bulk_add_convention("SAYC.txt")

# print(
#     hand_gen(
#         [[2, 4], [2, 4], [2, 6], [2, 6], [15, 17]],
#         [[0, 13], [0, 13], [0, 13], [0, 13], [0, 30]],
#         [[2, 3], [2, 3], [2, 5], [2, 5], [15, 17]],
#         [[0, 13], [0, 13], [0, 13], [0, 13], [0, 30]],
#     )
# )

# hand = [
#     card.from_card("AS"),
#     card.from_card("KS"),
#     card.from_card("AC"),
#     card.from_card("AD"),
# ]

# for i in hand:
#     print(i)

# car = card.from_card("JH")

# print(
#     are_requirements_being_achieved(
#         hand, [[2, 4], [2, 4], [2, 6], [2, 6], [15, 17]], car
#     )
# )
