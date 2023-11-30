from collections.abc import Iterator
from dataclasses import dataclass
from functools import reduce
from operator import or_

import numpy as np


@dataclass(frozen=True)
class Blizzard:
    position: tuple[int, ...]
    velocity: tuple[int, ...]


def step(coords: tuple[int, ...], blizzards: set[Blizzard], dimensions: tuple[int, ...], bonus: set[tuple[int, ...]]
         ) -> Iterator[tuple[int, ...]]:
    """
    Find all the positions accessible from a given position in one step, while avoiding blizzards
    :param coords: The coordinates of the start position
    :param blizzards: The blizzards representing positions that may not be moved into
    :param dimensions: The dimensions that bound the board
    :param bonus: The positions outside the dimensions that are nonetheless accessible
    :return: An iterator through the accessible positions
    """
    positions = {blizzard.position for blizzard in blizzards}
    if coords not in positions:
        yield coords
    for dimension in range(len(dimensions)):
        for delta in (-1, 1):
            check = coords[:dimension] + (coords[dimension] + delta,) + coords[dimension+1:]
            if all(0 <= c < d for c, d in zip(check, dimensions)) and check not in positions or check in bonus:
                yield check


def move_blizzards(blizzards: set[Blizzard], dimensions: tuple[int, ...]) -> set[Blizzard]:
    result = set()
    for blizzard in blizzards:
        position = tuple((pos + vel) % dim for pos, vel, dim in zip(blizzard.position, blizzard.velocity, dimensions))
        result.add(Blizzard(position, blizzard.velocity))
    return result


def search(start: tuple[int, ...], end: tuple[int, ...], blizzards: set[Blizzard], dimensions: tuple[int, ...]):
    curr = {start}
    steps = 0
    while True:
        if end in curr:
            break
        blizzards = move_blizzards(blizzards, dimensions)
        curr = reduce(or_, (set(step(coords, blizzards, dimensions, {start, end})) for coords in curr))
        steps += 1
    return steps, blizzards


def part_a(inp):
    """array
    split
    """
    inp = inp[1:-1, 1:-1]
    blizzards = {Blizzard(pos, (1, 0)) for pos in zip(*np.where(inp == "v"))}
    blizzards |= {Blizzard(pos, (-1, 0)) for pos in zip(*np.where(inp == "^"))}
    blizzards |= {Blizzard(pos, (0, 1)) for pos in zip(*np.where(inp == ">"))}
    blizzards |= {Blizzard(pos, (0, -1)) for pos in zip(*np.where(inp == "<"))}
    start, end = (-1, 0), (inp.shape[0], inp.shape[1] - 1)
    steps, _ = search(start, end, blizzards, inp.shape)
    return steps


def part_b(inp):
    """array
    split
    """
    inp = inp[1:-1, 1:-1]
    blizzards = {Blizzard(pos, (1, 0)) for pos in zip(*np.where(inp == "v"))}
    blizzards |= {Blizzard(pos, (-1, 0)) for pos in zip(*np.where(inp == "^"))}
    blizzards |= {Blizzard(pos, (0, 1)) for pos in zip(*np.where(inp == ">"))}
    blizzards |= {Blizzard(pos, (0, -1)) for pos in zip(*np.where(inp == "<"))}
    start, end = (-1, 0), (inp.shape[0], inp.shape[1] - 1)

    total = 0
    steps, blizzards = search(start, end, blizzards, inp.shape)
    total += steps
    steps, blizzards = search(end, start, blizzards, inp.shape)
    total += steps
    steps, blizzards = search(start, end, blizzards, inp.shape)
    total += steps
    return total
