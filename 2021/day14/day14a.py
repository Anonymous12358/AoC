def polymerise(polymer, rules):
    new_polymer = []
    last_element = None
    for element in polymer:
        if last_element is not None:
            new_polymer.append(rules[last_element, element])
        new_polymer.append(element)
        last_element = element
    return new_polymer


def process_inp(inp):
    polymer = inp[0]
    rules = {(line[0], line[1]): line[6] for line in inp[2:]}
    return polymer, rules


def main(inp):
    polymer, rules = process_inp(inp)
    for _ in range(10):
        polymer = polymerise(polymer, rules)
    counts = {polymer.count(element) for element in set(polymer)}
    return max(counts) - min(counts)
