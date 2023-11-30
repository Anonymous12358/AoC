from collections.abc import Iterator
from functools import reduce
from operator import or_

import numpy as np


def step(array: np.ndarray, coords: tuple[int, ...]) -> Iterator[tuple[int, ...]]:
    """
    Determine all places to which it is possible to move directly, from a given position in a given array.
    :param array: The array in which to move
    :param coords: The coordinates of the point from which to move. Must match the dimensionality of `array`.
    :return: An iterator through all locations that can be visited
    """
    height = array[coords]
    for dimension in range(len(coords)):
        for delta in (1, -1):
            result = coords[:dimension] + (coords[dimension] + delta,) + coords[dimension+1:]
            if 0 <= result[dimension] < array.shape[dimension] and array[result] <= height + 1:
                yield result


def traverse(array: np.ndarray, start: set[tuple[int, ...]], end: set[tuple[int, ...]]) -> int:
    """
    Find the shortest distance on a given array between any point in `start` and any point in `end`
    :param array: The array to traverse
    :param start: The set of start coordinates as tuples. Each tuple must match the dimensionality of `array`.
    :param end: The set of end coordinates as tuples.
    :return: The length of the shortest path.
    """
    visited = curr = start
    steps = 0
    while True:
        if curr & end:
            break
        # Make a move from all current locations at once
        curr = reduce(or_, (set(step(array, coords)) for coords in curr))
        # Discard locations that we could already reach more efficiently
        curr -= visited
        visited |= curr
        steps += 1
    return steps


def pre_process(inp):
    # Convert to array of ints
    array = np.array([[ord(char) - 96 for char in line] for line in inp])
    # Grab the start and end
    start = tuple(map(int, np.where(array == ord("S") - 96)))
    end = tuple(map(int, np.where(array == ord("E") - 96)))
    # Fix the start and end locations in the array
    array[np.where(array == ord("S") - 96)] = 0
    array[np.where(array == ord("E") - 96)] = 25

    return array, start, end


def part_a(inp):
    array, start, end = pre_process(inp)
    return traverse(array, {start}, {end})


def part_b(inp):
    array, _, end = pre_process(inp)
    return traverse(array, set(zip(*np.where(array == 0))), {end})
