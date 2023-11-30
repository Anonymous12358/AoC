def part_a(inp):
    # Preprocessing: convert each character to an int by indexing it within the list of letters
    """
    split
    int
    _abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    """
    total = 0
    for line in inp:
        # Bisect the string
        first, second = line[:len(line)//2], line[len(line)//2:]
        # Get the intersection of the two compartments, then get an arbitrary element of that set
        total += next(iter(set(first) & set(second)))
    return total


def part_b(inp):
    """
    split
    int
    _abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
    """
    total = 0
    # We take one iterator `map(set, inp)`, and triplicate it by tripling a tuple and unpacking
    # Each time we get the next element of the resulting iterator, the base iterator moves forward three
    # ie, we chomp through three elves at a time
    for elf1, elf2, elf3 in zip(*(map(set, inp),)*3):
        # Intersect all three elves and get an arbitrary element
        total += next(iter(elf1 & elf2 & elf3))

    return total
