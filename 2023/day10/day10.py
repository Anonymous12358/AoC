import itertools

import numpy as np


def leads_to(y, x, inp):
    char = inp[y, x]
    if char == "F":
        return {(y+1, x), (y, x+1)}
    elif char == "7":
        return {(y+1, x), (y, x-1)}
    elif char == "L":
        return {(y-1, x), (y, x+1)}
    elif char == "J":
        return {(y-1, x), (y, x-1)}
    elif char == "|":
        return {(y+1, x), (y-1, x)}
    elif char == "-":
        return {(y, x-1), (y, x+1)}
    else:
        return set()


def adjacent(y, x, shape):
    return [(y + dy, x + dx)
            for dy, dx in [(1, 0), (0, 1), (-1, 0), (0, -1)]
            if 0 <= y + dy < shape[0] and 0 <= x + dx < shape[1]]


def part_a(inp):
    """array
    split
    str"""
    start = tuple(np.argwhere(inp == "S")[0])
    # First step: find what points into S
    curr = {start}
    next_ = {(y, x) for y, x in adjacent(*start, inp.shape) if start in leads_to(y, x, inp)}

    # At each step after the first, look at what each of the current cells point to
    for i in itertools.count(1):
        curr, next_ = next_, {
            (y, x) for cell in next_ for y, x in adjacent(*cell, inp.shape)
            if (y, x) not in curr and (y, x) in leads_to(*cell, inp)
        }
        if not next_:
            break
    return i


def part_b(inp):
    """array
    split
    str"""
    # Filter out irrelevant pipes
    start = tuple(np.argwhere(inp == "S")[0])
    curr = {(y, x) for y, x in adjacent(*start, inp.shape) if start in leads_to(y, x, inp)}
    seen = {start}

    while curr:
        seen |= curr
        curr = {
            (y, x) for cell in curr for y, x in adjacent(*cell, inp.shape)
            if (y, x) not in seen and (y, x) in leads_to(*cell, inp)
        }

    for y in range(inp.shape[0]):
        for x in range(inp.shape[1]):
            if (y, x) not in seen:
                inp[y, x] = "."

    # Determine what the start tile is meant to be
    if start in leads_to(start[0] + 1, start[1], inp):
        if start in leads_to(start[0] - 1, start[1], inp):
            inp[start] = "|"
        elif start in leads_to(start[0], start[1] + 1, inp):
            inp[start] = "F"
        else:
            inp[start] = "7"
    elif start in leads_to(start[0] - 1, start[1], inp):
        if start in leads_to(start[0], start[1] + 1, inp):
            inp[start] = "L"
        else:
            inp[start] = "J"
    else:
        inp[start] = "-"

    result = 0
    for y, row in enumerate(inp):
        inside = False
        pipe_entered = None
        for x, char in enumerate(row):
            if char in "FL":
                pipe_entered = char
            elif (pipe_entered, char) in (("F", "7"), ("L", "J")):
                pipe_entered = None
            elif (pipe_entered, char) in (("F", "J"), ("L", "7")):
                pipe_entered = None
                inside = not inside
            if char == ".":
                result += inside
            elif char == "|":
                inside = not inside

    return result
