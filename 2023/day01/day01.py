def part_a(inp):
    r"""
    /.*?(\d)(?:.*(\d))?.*/
    int int
    """
    return sum((a*10 + b) if b is not None else a*11 for (a, b) in inp)


def to_int(s):
    if s is None:
        return None
    elif s.isdigit():
        return int(s)
    else:
        return ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"].index(s)


def part_b(inp):
    r"""
    /.*?(\d|one|two|three|four|five|six|seven|eight|nine)(?:.*(\d|one|two|three|four|five|six|seven|eight|nine))?.*/
    """
    inp = [(to_int(a), to_int(b)) for (a, b) in inp]
    return sum((a * 10 + b) if b is not None else a * 11 for (a, b) in inp)
