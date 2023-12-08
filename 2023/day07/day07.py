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
    # Separate jokers
    jokers = hand.count("J")
    hand = tuple(c for c in hand if c != "J")
    # We only need to iterate through values that already occur in the hand
    in_hand = set(hand)
    if not in_hand:
        in_hand = {"2"}
    # Iterate over all values of the jokers and return the best achievable hand
    return max(categorise(hand + joker_values) for joker_values in itertools.product(in_hand, repeat=jokers))


def rate_b(hand):
    return categorise_b(hand), *map("J23456789TQKA".index, hand)


def part_b(inp):
    r"""
    /([23456789TJQKA]{5}) (\d+)/
    str int
    """
    inp = sorted(inp, key=lambda row: rate_b(row[0]))
    return sum((i + 1) * bid for i, (_, bid) in enumerate(inp))
