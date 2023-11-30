def deterministic_die():
    result = 0
    while True:
        result = result % 100 + 1
        yield result


def game(starts, die_factory):
    rolls = 0
    positions = list(starts)
    scores = [0] * len(positions)
    die = die_factory()
    while True:
        for i in range(len(positions)):
            rolls += 3
            positions[i] = (positions[i] + sum(next(die) for _ in range(3)) - 1) % 10 + 1
            scores[i] += positions[i]
            if scores[i] >= 1000:
                return min(scores) * rolls


def parse_inp(inp):
    return tuple(int(line[28:]) for line in inp)


def main(inp):
    return game(parse_inp(inp), deterministic_die)
