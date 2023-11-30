def part_a(inp):
    score = 0
    for line in inp:
        # ord(line[2]) - 88 gets the number of the choice we played (0 for rock etc)
        score += ord(line[2]) - 88 + 1
        # ord(line[0]) - 65 + 1 is one more than what opponent played - ie, what needs to be played to beat them
        if ord(line[2]) - 88 == (ord(line[0]) - 65 + 1) % 3:
            # We win
            score += 6
        elif ord(line[2]) - 88 == ord(line[0]) - 65:
            # We tie
            score += 3
    return score


def part_b(inp):
    score = 0
    for line in inp:
        # Reverse-engineer what we played
        score += (ord(line[0]) - 65 + ord(line[2]) - 88 - 1) % 3 + 1
        # Reward
        score += 3 * (ord(line[2]) - 88)
    return score


def part_b_alt(inp):
    # An easier, if less extensible, solution is to hard-code the score change for each case
    # Nicely, the score changes are all distinct, and consecutive, so we can just index from a list
    score_change = [None, "B X", "C X", "A X", "A Y", "B Y", "C Y", "C Z", "A Z", "B Z"]
    return sum(map(score_change.index, inp))
