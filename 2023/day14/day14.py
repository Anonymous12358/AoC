import itertools

import numpy as np


def roll(arr, axis, direct):
    if axis == 0:
        arr = arr.T
    if direct == 1:
        arr = arr[:, ::-1]

    for row in arr:
        fall_pos = 0
        for i, char in enumerate(row):
            if char == "#":
                fall_pos = i + 1
            elif char == "O":
                row[i] = "."
                row[fall_pos] = "O"
                fall_pos += 1


def get_load(arr):
    result = 0
    for (y, _), char in np.ndenumerate(arr):
        if char == "O":
            result += arr.shape[0] - y

    return result


def part_a(inp):
    """array
    split
    str"""
    roll(inp, 0, -1)
    return get_load(inp)


def freeze(arr, axis, direct):
    return tuple(map(tuple, arr)), axis, direct


def part_b(inp):
    """array
    split
    str"""
    seen = {}
    # 4 billion steps for 1b full cycles
    go_until = 4_000_000_000
    for i, (axis, direct) in enumerate(itertools.cycle(((0, -1), (1, -1), (0, 1), (1, 1)))):
        frozen = freeze(inp, axis, direct)
        if frozen in seen and go_until == 4_000_000_000:
            cycle_start, cycle_length = seen[frozen], i - seen[frozen]
            remainder = (4_000_000_000 - cycle_start) % cycle_length
            go_until = i + remainder
        if i == go_until:
            break
        seen[frozen] = i
        roll(inp, axis, direct)

    return get_load(inp)
