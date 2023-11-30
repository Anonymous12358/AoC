from collections import defaultdict


def polymerise(pairs, rules):
    new_pairs = defaultdict(int)
    for pair, count in pairs.items():
        new_pairs[pair[0], rules[pair]] += count
        new_pairs[rules[pair], pair[1]] += count
    return new_pairs


def process_inp(inp):
    pairs_list = zip(inp[0], inp[0][1:])
    pairs = defaultdict(int)
    for pair in pairs_list:
        pairs[pair] += 1

    rules = {(line[0], line[1]): line[6] for line in inp[2:]}
    return pairs, rules


def main(inp):
    elements = "BCFHKNOPSV"
    pairs, rules = process_inp(inp)
    last = inp[0][-1]
    for _ in range(40):
        pairs = polymerise(pairs, rules)
    counts = {element: sum(pairs[element, other_element] for other_element in elements) for element in elements}
    counts[last] += 1
    return max(counts.values()) - min(counts.values())
