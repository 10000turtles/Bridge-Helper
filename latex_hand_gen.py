import string


def append_cards(suit, delim, s):
    for card in suit:
        s = s + cards[card] + delim

    return s


spades = "K842"
hearts = "9"
diamonds = "KQJT974"
clubs = "K"

cards = {
    "2": "\crdtwo",
    "3": "\crdtre",
    "4": "\crdfour",
    "5": "\crdfive",
    "6": "\crdsix",
    "7": "\crdsev",
    "8": "\crdeig",
    "9": "\crdnine",
    "T": "\crdten",
    "J": "\crdJ",
    "Q": "\crdQ",
    "K": "\crdK",
    "A": "\crdA",
}

order = [(spades, "s"), (hearts, "h"), (clubs, "c"), (diamonds, "d")]

if len(hearts) == 0:
    order = [(spades, "s"), (diamonds, "d"), (clubs, "c")]

if len(clubs) == 0:
    order = [(hearts, "d"), (spades, "s"), (diamonds, "c")]

s = "\\begin{cards}\scalebox{.6}{"

for suit, delim in order:
    print(suit + " " + delim)
    s = append_cards(suit, delim, s)

s = s + "\\}end{cards}"
print(s)
print()
