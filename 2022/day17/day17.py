import itertools
from collections.abc import Iterable, Sequence

import numpy as np

ROCKS = [
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],
    [(0, 2), (1, 2), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(0, 0), (0, 1), (1, 0), (1, 1)]
]
JETS = {">": (0, 1), "<": (0, -1)}
chomped = 0


def add(*tuples: tuple) -> tuple:
    return tuple(map(sum, zip(*tuples)))


def try_move(array: np.ndarray, rock: Sequence[tuple[int, ...]], pos: tuple[int, ...], delta: tuple[int, ...]
             ) -> tuple[tuple[int, ...], bool]:
    """
    Attempt to move a rock within a given array. The rock moves if its new position is entirely within the array and
    the array is entirely 0 where the rock is.
    :param array: The array in which to move
    :param rock: A sequence containing the coordinates of each part of the rock, relative to its top-left corner
    :param pos: The position of the top-left corner of the rock in the array
    :param delta: The vector by which to move the rock
    :return: The new position of the rock, and whether or not the vector was applied
    """

    new_pos = add(pos, delta)
    # Check rock in bounds
    for i, (ordinate, length) in enumerate(zip(new_pos, array.shape)):
        # We allow the rock to be above the array in the 0th dimension, but not in any other
        if i > 0 and ordinate < 0:
            return pos, False
        if ordinate + max(rock_part[i] for rock_part in rock) >= length:
            return pos, False
    # Check rock doesn't intersect
    for rock_part in rock:
        if new_pos[0] + rock_part[0] >= 0 and array[add(new_pos, rock_part)] != 0:
            return pos, False
    return new_pos, True


def drop_rock(array: np.ndarray, rock: Sequence[tuple[int, ...]], deltas: Iterable[tuple[int, ...]]) -> tuple[int, ...]:
    global chomped

    # We start with the bottom of the rock at the top of the array
    pos = -max(rock_part[0] for rock_part in rock), 2
    for delta in deltas:
        chomped = (chomped + 1) % 10_091
        pos, _ = try_move(array, rock, pos, delta)
        pos, did_fall = try_move(array, rock, pos, (1, 0))
        if not did_fall:
            break
    return pos


def get_height(array: np.ndarray) -> int:
    result = array.shape[0]
    for i in range(result):
        if np.any(array[i]):
            break
        else:
            result -= 1

    return result


def part_a(raw_inp):
    array = np.zeros((0, 7), dtype='int32')
    deltas = itertools.cycle(map(JETS.__getitem__, raw_inp))
    pos = 0, 0
    for i, rock in zip(range(2022), itertools.cycle(ROCKS)):
        # Expand the array to accommodate the next rock
        # pos is the coordinates of the top-left corner of the rock. If pos.y < 4, it is the highest point in the array,
        # since any rocks placed there previously would already have resulted in padding. Therefore padding by 4 - pos.y
        # allows the bottom of the rock to be at y=0.
        pad_height = max(4 - pos[0], 0)
        array = np.pad(array, ((pad_height, 0), (0, 0)))

        # Place the rock
        pos = drop_rock(array, rock, deltas)
        for rock_part in rock:
            array[add(pos, rock_part)] = 1

    return get_height(array)


def part_b(raw_inp):
    array = np.zeros((0, 7), dtype='int32')
    deltas = itertools.cycle(map(JETS.__getitem__, raw_inp))
    pos = 0, 0
    for i, rock in zip(range(140 + 1735 * 20), itertools.cycle(ROCKS)):
        # Expand the array to accommodate the next rock
        # pos is the coordinates of the top-left corner of the rock. If pos.y < 4, it is the highest point in the array,
        # since any rocks placed there previously would already have resulted in padding. Therefore padding by 4 - pos.y
        # allows the bottom of the rock to be at y=0.
        pad_height = max(4 - pos[0], 0)
        array = np.pad(array, ((pad_height, 0), (0, 0)))

        if i % 1735 == 140:
            print(f"rocks={i} {chomped=} height={get_height(array)}")

        # Place the rock
        pos = drop_rock(array, rock, deltas)
        for rock_part in rock:
            array[add(pos, rock_part)] = 1

    print(f"rocks={140 + 1735 * 20} {chomped=} height={get_height(array)}")

    return get_height(array)
