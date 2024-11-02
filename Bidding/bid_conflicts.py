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


def grouper(n, iterable, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


def find_intersection(first, second):
    l = first[0]
    r = first[1]

    if second[0] > r or second[1] < l:
        return [0, -1]

    else:
        l = max(l, second[0])
        r = min(r, second[1])

    return [l, r]


def generate_shapes(shape, point_range):
    shapes = []
    for s in range(shape[0][0], shape[0][1] + 1, 1):
        for h in range(s + shape[1][0], min(s + shape[1][1] + 1, 14), 1):
            for d in range(h + shape[2][0], min(h + shape[2][1] + 1, 14), 1):
                c = 13 - d
                if c > shape[3][1] or c < shape[3][0]:
                    continue
                shapes.append([s, h - s, d - h, c, point_range[0], point_range[1]])

    return shapes


def does_shape_fit_desc(shape, desc):
    # print()
    # print(shape)
    # print(desc)
    for i in range(0, 4, 1):
        if shape[i] < desc[i][0] or shape[i] > desc[i][1]:
            return False

    return True


def conflict(h_a, h_b):
    shapes = []
    for thing in h_a:
        shapes = shapes + generate_shapes(thing[0:4], thing[4])

    conflicts = []
    for s in shapes:
        for hand in h_b:
            if does_shape_fit_desc(s, hand):
                intersecting_point_range = find_intersection([s[4], s[5]], hand[4])
                if intersecting_point_range[1] - intersecting_point_range[0] > 0:
                    conflicts.append(s)
                    conflicts[-1][4] = intersecting_point_range[0]
                    conflicts[-1][5] = intersecting_point_range[1]

    return conflicts


sequence = ""
filename = "SAYC.txt"

responses = []

hands = []


with open(filename, "r") as input:
    s = input.read()
    inputs = ("".join(s.split())).split(":")

    for seq, b, desc in list(grouper(3, inputs)):
        if sequence == seq:
            responses.append(b)
            hands.append(literal_eval(desc))

total_resp = len(responses)

for i in range(0, total_resp, 1):
    for j in range(i + 1, total_resp, 1):
        conflicting_shapes = conflict(hands[i], hands[j])
        if len(conflicting_shapes) > 0:
            for shape in conflicting_shapes:
                print(
                    responses[i],
                    " and ",
                    responses[j],
                    " share the shape ",
                    shape[0:4],
                    " with point range ",
                    shape[4],
                    " to ",
                    shape[5],
                    ".",
                )
