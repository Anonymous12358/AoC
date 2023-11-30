import numpy as np


def preprocess(inp) -> np.ndarray:
    # The array is transposed to be row-major
    # We could crop the array to improve performance but it runs fast enough in this case anyway
    array = np.zeros((200, 1000), dtype=np.int16)
    for line in inp:
        start, _, rest = line.partition(" -> ")
        start_x, start_y = map(int, start.split(","))
        for end in rest.split(" -> "):
            end_x, end_y = map(int, end.split(","))
            y_direct, x_direct = 1 - 2*(start_y > end_y), 1 - 2*(start_x > end_x)
            array[start_y:end_y+y_direct:y_direct, start_x:end_x+x_direct:x_direct] = 1
            start_x, start_y = end_x, end_y

    return array


def place_sand(array: np.ndarray, sand_source: tuple[int, ...], deltas: list[tuple[int, ...]]
               ) -> tuple[int, ...] | None:
    """
    Find the position at which to place a grain of sand in a given array
    :param array: The array in which to place. 0 represents a valid location to place at.
    :param sand_source: The coordinates at which the sand spawns. Must match the dimensionality of array.
    :param deltas: The ways in which the sand may move. It follows the first vector it can in the list, or settles if
        it can't follow any. Tuples must match the dimensionality of array.
    :return: The coordinates at which the sand settles, or None if it reaches the edge without settling.
    """
    coords = sand_source
    # This code is supposed to be generified, but we can't tell for a general list of deltas whether a grain at a given
    # position will ever settle, so this line cheats based on knowledge of the broader puzzle.
    # We assume that if it nears the bottom edge it will never settle
    while all(0 <= ordinate < length - 1 for ordinate, length in zip(coords, array.shape)):
        for delta in deltas:
            check = tuple(map(sum, zip(coords, delta)))
            if array[check] == 0:
                coords = check
                break
        else:
            return coords
    return None


def part_a(inp):
    array = preprocess(inp)
    i = 0
    while True:
        coords = place_sand(array, (0, 500), [(1, 0), (1, -1), (1, 1)])
        if coords is None:
            return i
        array[coords] = 2
        i += 1


def part_b(inp):
    array = preprocess(inp)
    lowest = max(np.where(array == 1)[0])
    array[lowest + 2, :] = 1

    i = 0
    while True:
        coords = place_sand(array, (0, 500), [(1, 0), (1, -1), (1, 1)])
        if coords is None:
            print("Panic")
        array[coords] = 2
        i += 1
        if coords == (0, 500):
            return i
