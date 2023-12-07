import collections
import itertools


def categorise(hand):
    counter = collections.Counter(collections.Counter(hand).values())
    if 5 in counter:
        return 6
    elif 4 in counter:
        return 5
    elif collections.Counter({2: 1, 3: 1}) <= counter:
        return 4
    elif 3 in counter:
        return 3
    elif collections.Counter({2: 2}) <= counter:
        return 2
    elif 2 in counter:
        return 1
    else:
        return 0


def rate(hand):
    return categorise(hand), *map("23456789TJQKA".index, hand)


def part_a(inp):
    r"""
    /([23456789TJQKA]{5}) (\d+)/
    str int
    """
    inp = sorted(inp, key=lambda row: rate(row[0]))
    return sum((i+1) * bid for i, (_, bid) in enumerate(inp))


def categorise_b(hand):
    jokers = hand.count("J")
    # Move jokers to the front
    hand = list(sorted(hand, key=lambda c: c != "J"))
    # We only need to iterate through values that already occur in the hand
    in_hand = set(hand)
    in_hand.discard("J")
    if not in_hand:
        in_hand = {"2"}
    best = 0
    # Iterate through all possible values of the jokers
    for joker_values in itertools.product(in_hand, repeat=jokers):
        hand[:jokers] = joker_values
        best = max(best, categorise(hand))
    return best


def rate_b(hand):
    return categorise_b(hand), *map("J23456789TQKA".index, hand)


def part_b(inp):
    r"""
    /([23456789TJQKA]{5}) (\d+)/
    str int
    """
    inp = sorted(inp, key=lambda row: rate_b(row[0]))
    return sum((i + 1) * bid for i, (_, bid) in enumerate(inp))
