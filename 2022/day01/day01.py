def part_a(raw_inp):
    return max(sum(map(int, elf.split("\n"))) for elf in raw_inp.split("\n\n"))


def part_b(raw_inp):
    # Sorts the whole list - inefficient, but fine in this case and leads to shorter code
    return sum(sorted(sum(map(int, elf.split("\n"))) for elf in raw_inp.split("\n\n"))[-3:])


def part_b_alt(raw_inp):
    # Maintain a leaderboard of the top three foods
    maxes = {-3, -2, -1}
    for elf in raw_inp.split("\n\n"):
        food = sum(map(int, elf.split("\n")))
        # Knock the smallest off the leaderboard when a new max comes
        if food > min(maxes):
            maxes.remove(min(maxes))
            maxes.add(food)

    return sum(maxes)
