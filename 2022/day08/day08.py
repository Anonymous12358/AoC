from functools import reduce
from operator import or_

import numpy as np


def shift_and_accumulate(array: np.ndarray, axis: int, amount: int) -> np.ndarray:
    """
    Shift an array a certain distance along a certain axis, padding with -1, then accumulate np.maximum over the array
    in that axis, so that every value is replaced with the maximum in that polytelon up to that point.

    The resulting array has the same shape as the input array; data that are shifted off the end of the array are
    discarded. Operates out-of-place.
    :param array: The array on which to operate.
    :param axis: The axis along which to shift.
    :param amount: The distance by which to shift. If negative, shifts and accumulates in the negative direction.
    :return: The shifted and accumulated array.
    """
    indices = tuple(
        slice(-amount if amount < 0 else None, -amount if amount > 0 else None)
        if i == axis else Ellipsis
        for i in range(2)
    )
    padding = tuple(
        (max(amount, 0), -min(amount, 0))
        if i == axis else (0, 0)
        for i in range(2)
    )
    shifted = np.pad(array[indices], padding, constant_values=-1)
    if amount > 0:
        shifted = np.maximum.accumulate(shifted, axis=axis)
    else:
        shifted = np.flip(np.maximum.accumulate(np.flip(shifted, axis=axis), axis=axis), axis=axis)
    return shifted


def part_a(inp):
    """array
    split
    int
    """
    # We compare each tree to the maximum height of any tree before it in the same line (column in the 2d case), in
    # each dimension.
    # This is achieved through the shift_and_accumulate function with an amount of 1 or -1.
    # We then `|` the arrays together to collect all trees that are visible from any direction.
    return np.count_nonzero(reduce(
        or_,
        (inp > shift_and_accumulate(inp, axis, amount)
         for axis in range(inp.ndim)
         for amount in (1, -1))
    ))


def scenic_score(array: np.ndarray, coords: tuple[int, ...]) -> int:
    """
    Compute the scenic score of the tree at a given position in a given array.
    :param array: The array on which to operate.
    :param coords: The coordinates of the tree to consider.
    :return: The scenic score of the tree.
    """
    # 0s in the coordinates cause coords[axis]+direction to loop round to -1
    # Fortunately we can filter them out immediately
    if 0 in coords:
        return 0

    result = 1
    # We construct a line through the coords, orthogonal in each dimension
    # To see how to construct also the diagonal lines, see:
    # https://github.com/Anonymous12358/NEA/blob/master/pente/game/Board.py
    for axis in range(array.ndim):
        # Our index is equal to `coords` in every dimension except that through which the line travels
        line = array[tuple(slice(None) if i == axis else ordinate for i, ordinate in zip(range(array.ndim), coords))]

        for direction in (-1, 1):
            # Step through the line in each direction, breaking when we find a tree that obstructs our view
            count = 0
            # We start 1 after the centre tree and step in the correct direction
            for height in line[coords[axis]+direction::direction]:
                count += 1
                if height >= array[coords]:
                    break
            result *= count

    return result


def part_b(inp):
    """array
    split
    int
    """

    return max(scenic_score(inp, coords) for coords in np.ndindex(inp.shape))
