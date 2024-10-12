import string


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


test_1 = "P P P 1H P P X P P XX"
test_2 = "1H 1S 1NT X P"
test_3 = "1H 1S 3NT X P P"
test_4 = "1H"

print(valid_bids(str_to_sequence(test_1)))
print(valid_bids(str_to_sequence(test_2)))
print(valid_bids(str_to_sequence(test_3)))
print(valid_bids(str_to_sequence(test_4)))


class convention:
    def __init__(self, bidding_sequence):
        self.bidding_sequence = bidding_sequence

        self.responses = valid_bids(bidding_sequence)


def describe_hands(bids, dealer, NS_System, EW_System):
    return
