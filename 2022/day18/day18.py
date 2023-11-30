from collections.abc import Iterator
from functools import reduce
from operator import or_


def step(coords: tuple[int, ...]) -> Iterator[tuple[int, ...]]:
    """
    Determine all places to which it is possible to move directly from a given position.
    :param coords: The coordinates of the point from which to move.
    :return: An iterator through all locations that can be visited
    """
    for dimension in range(len(coords)):
        for delta in (1, -1):
            yield coords[:dimension] + (coords[dimension] + delta,) + coords[dimension+1:]


def part_a(inp):
    r"""
    /(\d+),(\d+),(\d+)/
    int
    """
    return sum(face not in inp for cube in inp for face in step(cube))


def check_face(start: tuple[int, ...], cubes: set[tuple[int, ...]]) -> bool:
    """
    Determine whether there is a path from `start` to the point at infinity.
    :param start: The start coordinates.
    :param cubes: A set of cubes that block the path.
    :return: Whether there is a path.
    """
    if start in cubes:
        return False
    visited = curr = {start}
    while curr:
        if any(any(not 0 <= ordinate < 22 for ordinate in coords) for coords in curr):
            return True
        # Make a move from all current locations at once
        curr = reduce(or_, (set(step(coords)) for coords in curr))
        # Discard illegal moves
        curr -= cubes
        # Discard locations that we could already reach more efficiently
        curr -= visited
        visited |= curr
    return False


def part_b(inp):
    r"""
    /(\d+),(\d+),(\d+)/
    int
    """
    inp = set(inp)
    total = 0
    for i, cube in enumerate(inp):
        if any(not 0 <= ordinate < 22 for ordinate in cube):
            print(cube)
        if not i % 200:
            print(i)
        for face in step(cube):
            total += check_face(face, inp)
    return total
