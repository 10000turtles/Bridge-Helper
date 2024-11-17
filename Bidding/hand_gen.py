import string
import tracemalloc
from memory_profiler import profile
import pickle
from ast import literal_eval
import itertools
from itertools import zip_longest
import time
import pydealer
import math
import random


suit_key = {"Spades": 0, "Hearts": 1, "Diamonds": 2, "Clubs": 3}
value_key = {
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
    "Ace": 1,
}


def points(hand):
    jacks = len([i for i in hand if value_key[i.value] == 11])
    queens = len([i for i in hand if value_key[i.value] == 12])
    kings = len([i for i in hand if value_key[i.value] == 13])
    aces = len([i for i in hand if value_key[i.value] == 1])

    return aces * 4 + kings * 3 + queens * 2 + jacks


def does_violate_conditions(hand, description, card):
    pts = points(hand)

    if len(hand) > 12:
        return True

    if pts + points([card]) > description[4][1]:
        return True

    suit_len = len([i for i in hand if suit_key[i.suit] == suit_key[card.suit]])
    if suit_len + 1 > description[suit_key[card.suit]][1]:
        return True

    return False


def are_requirements_being_achieved(hand, description, card):
    print(hand)

    suit_len = len([i for i in hand if suit_key[i.suit] == suit_key[card.suit]])
    pts = points(hand)

    print(hand)
    print(pts)

    if (pts < description[4][0]) and (pts + points([card]) <= description[4][1]):
        if suit_len + 1 <= description[suit_key[card.suit]][0]:
            return True

    return False


def put_to_string(hand):

    rank_to_str = ["", "A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
    spade_str = ""
    heart_str = ""
    diamond_str = ""
    club_str = ""

    for i in hand:
        if suit_key[i.suit] == 0:
            spade_str = spade_str + rank_to_str[value_key[i.value]]

    for i in hand:
        if suit_key[i.suit] == 1:
            heart_str = heart_str + rank_to_str[value_key[i.value]]

    for i in hand:
        if suit_key[i.suit] == 2:
            diamond_str = diamond_str + rank_to_str[value_key[i.value]]

    for i in hand:
        if suit_key[i.suit] == 3:
            club_str = club_str + rank_to_str[value_key[i.value]]

    return spade_str + ":" + heart_str + ":" + diamond_str + ":" + club_str


def face_cards():
    deck = pydealer.Deck()
    deck.shuffle()

    terms = ["A", "K", "Q", "J"]

    face = deck.get_list(terms)

    random.shuffle(face)

    return face


def spot_cards():
    deck = pydealer.Deck()
    deck.shuffle()

    terms = ["2", "3", "4", "5", "6", "7", "8", "9", "10"]
    spot = deck.get_list(terms)

    random.shuffle(spot)

    return spot


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

    face = face_cards()
    spot = spot_cards()

    for card in face:
        random.shuffle(deal)

        for pos in deal:
            if are_requirements_being_achieved(pos[0], pos[1], card):
                pos[0].append(card)
                continue

        for pos in deal:
            if not does_violate_conditions(pos[0], pos[1], card):
                pos[0].append(card)
                continue

        west_cards.append(card)

    for card in spot:
        random.shuffle(deal)

        for pos in deal:
            if are_requirements_being_achieved(pos[0], pos[1], card):
                pos[0].append(card)
                continue

        for pos in deal:
            if not does_violate_conditions(pos[0], pos[1], card):
                pos[0].append(card)
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
#         [[0, 13], [0, 13], [0, 13], [0, 13], [0, 30]],
#         [[0, 13], [0, 13], [0, 13], [0, 13], [0, 30]],
#     )
# )

dec = pydealer.Deck()

hand = dec.get_list(["Ace of Spaces", "2 of spades"])

card = dec.get_list(["4 of Spades"])

print(hand)

print(
    are_requirements_being_achieved(
        hand, [[2, 4], [2, 4], [2, 6], [2, 6], [15, 17]], card
    )
)
