import numpy as np


def check_mirror(arr: np.ndarray, axis, x) -> bool:
    reflected = arr[(slice(None),) * axis + (slice(x - 1, None, -1),)]
    rest = arr[(slice(None),) * axis + (slice(x, None, 1),)]

    if rest.shape[axis] < reflected.shape[axis]:
        reflected = reflected[(slice(None),) * axis + (slice(rest.shape[axis]),)]
    else:
        rest = rest[(slice(None),) * axis + (slice(reflected.shape[axis]),)]

    return (reflected == rest).all()


def find_mirrors(arr: np.ndarray):
    for axis in range(2):
        # Starting from 1 so we don't find the line of reflection that's outside the grid on the left
        for x in range(1, arr.shape[axis]):
            if check_mirror(arr, axis, x):
                yield axis, x


def part_a(inp):
    """raw"""

    result = 0
    for i, arr_str in enumerate(inp.split("\n\n")):
        arr = np.array(list(map(list, arr_str.split("\n")))) == "#"

        for axis, x in find_mirrors(arr):
            result += x * (100 - 99 * axis)

    return result


def smudge(arr: np.ndarray):
    """Yield all arrays that differ from the input in precisely one place"""
    prev = None
    for coords in np.ndindex(*arr.shape):
        if prev is not None:
            arr[prev] = not arr[prev]
        arr[coords] = not arr[coords]
        prev = coords
        yield arr


def part_b(inp):
    """raw"""

    result = 0
    for i, arr_str in enumerate(inp.split("\n\n")):
        arr = np.array(list(map(list, arr_str.split("\n")))) == "#"
        original_mirror = next(find_mirrors(arr))
        for smudged in smudge(arr):
            mirrors = list(filter(lambda mirror: mirror != original_mirror, find_mirrors(smudged)))
            if mirrors:
                axis, x = mirrors[0]
                result += x * (100 - 99 * axis)
                break

    return result
