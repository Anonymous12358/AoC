from collections import defaultdict

import numpy as np


def part_a(inp):
    r"""array
    split
    int
    0123456789.*#+-/%=@&$
    """
    result = 0
    width = inp.shape[1]
    for y, x in np.ndindex(inp.shape):
        if x > 0 and inp[(y, x-1)] < 10:
            continue
        number_coords = []
        for x2 in range(x, width):
            if inp[y, x2] < 10:
                number_coords.append((y, x2))
            else:
                break
        search = {(y + dy, x + dx)
                  for dy in range(-1, 2) for dx in range(-1, 2)
                  for (y, x) in number_coords
                  if 0 <= y + dy < inp.shape[0] and 0 <= x + dx < width}
        if all(inp[coords] <= 10 for coords in search):
            continue

        digits = [inp[coords] for coords in number_coords]
        number = 0
        for digit in digits:
            number *= 10
            number += digit
        result += number
    return result


def part_b(inp):
    r"""array
    split
    int
    0123456789.*#+-/%=@&$
    """
    width = inp.shape[1]
    gears = defaultdict(list)
    for y, x in np.ndindex(inp.shape):
        if x > 0 and inp[(y, x - 1)] < 10:
            continue
        number_coords = []
        for x2 in range(x, width):
            if inp[y, x2] < 10:
                number_coords.append((y, x2))
            else:
                break
        search = {(y + dy, x + dx)
                  for dy in range(-1, 2) for dx in range(-1, 2)
                  for (y, x) in number_coords
                  if 0 <= y + dy < inp.shape[0] and 0 <= x + dx < width}
        digits = [inp[coords] for coords in number_coords]
        number = 0
        for digit in digits:
            number *= 10
            number += digit
        adjacent_gears = [coords for coords in search if inp[coords] == 11]
        for gear in adjacent_gears:
            gears[gear].append(number)

    return sum(gear[0] * gear[1] for gear in gears.values() if len(gear) == 2)
