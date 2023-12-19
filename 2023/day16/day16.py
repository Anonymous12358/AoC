import functools
import operator


def part_a(inp):
    """array
    split
    str"""

    # Set of (y, x), (dy, dx) pairs
    beams = {((0, -1), (0, 1))}
    return calc_energy(beams, inp)


def calc_energy(beams, inp):
    energized = set()
    seen = set()
    while beams:
        if not beams:
            break
        seen |= beams
        # omg another concatmap
        beams = functools.reduce(operator.or_, [step(beam, inp) for beam in beams])
        beams -= seen
        energized |= {pos for pos, _ in beams}

    return len(energized)


def step(beam, inp):
    (y, x), (dy, dx) = beam
    y += dy
    x += dx
    if not (0 <= y < inp.shape[0] and 0 <= x < inp.shape[1]):
        return set()
    if inp[y][x] == "\\":
        return {((y, x), (dx, dy))}
    elif inp[y][x] == "/":
        return {((y, x), (-dx, -dy))}
    elif inp[y][x] == "|" and dy == 0:
        return {((y, x), (1, 0)), ((y, x), (-1, 0))}
    elif inp[y][x] == "-" and dx == 0:
        return {((y, x), (0, 1)), ((y, x), (0, -1))}

    return {((y, x), (dy, dx))}


def part_b(inp):
    """array
    split
    str"""
    max_ = 0
    for y in range(inp.shape[0]):
        print(y)
        max_ = max(max_, calc_energy({((y, -1), (0, 1))}, inp))
        print(y)
        max_ = max(max_, calc_energy({((y, inp.shape[1]), (0, -1))}, inp))
    for x in range(inp.shape[1]):
        print(x)
        max_ = max(max_, calc_energy({((-1, x), (1, 0))}, inp))
        print(x)
        max_ = max(max_, calc_energy({((inp.shape[0], x), (-1, 0))}, inp))

    return max_
