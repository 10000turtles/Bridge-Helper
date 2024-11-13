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
from bidding import system

def does_violate_conditions(hand,description,card):
    return 

def are_requirements_being_achieved(hand,description,card):
    return

def face_cards() -> deck_of_cards.DeckOfCards:
    return
def spot_cards():
    return 
def hand_gen(north,east,south,west):

    north_cards = []
    east_cards = []
    south_cards = []
    west_cards = []

    face = face_cards()
    spot = spot_cards()

    for i in range(0,16,1):
        card = face.give_random_card()

        if(are_requirements_being_achieved(north_cards,north,card)):
            north_cards.append(card)
        elif(does_violate_conditions(north_cards,north,card)):
            

    return


sayc = system()
sayc.bulk_add_convention("SAYC.txt")
