import numpy as np


def part_a(inp):
    """quick array"""
    # Simulate dark energy
    # idk quite why the axes are swapped
    inp = np.insert(inp, *(inp == 0).all(axis=0).nonzero(), 0, axis=1)
    inp = np.insert(inp, *(inp == 0).all(axis=1).nonzero(), 0, axis=0)

    result = 0
    # Number of galaxies
    n = np.sum(inp)

    # The total distance in each axis is sum{i = 0; n-1} sum{j=i; n-1} |x_i - x_j|
    # = sum{i=0; n-1} sum{j=i; n-1} x_j - x_i as long as the xs are sorted in ascending order
    # = sum{j = 0; n-1} x_j * j + sum{i = 0; n - 1} x_i * (n - i - 1) counting the no of times each term appears
    # = sum{i = 0; n - 1} x_i * (i - (n - i - 1))
    # = sum{i = 0 n - 1} x_i * (2i-n + 1)
    for i, (y, _) in enumerate(np.argwhere(inp != 0)):
        result += y * (2 * i - n + 1)
    for i, (x, _) in enumerate(np.argwhere(inp.T != 0)):
        result += x * (2 * i - n + 1)
    return result


def part_b(inp):
    """quick array"""
    return count_in_axis(inp, 0) + count_in_axis(inp, 1)


def count_in_axis(inp, axis, dark_energy_strength=999_999):
    result = 0
    n = np.sum(inp)
    galaxies_seen, empties_seen = 0, 0
    for ordinate, line in enumerate(np.moveaxis(inp, axis, 0)):
        count = np.sum(line)
        if count == 0:
            empties_seen += 1
        else:
            result += (ordinate + dark_energy_strength * empties_seen) * (2 * galaxies_seen - n + count) * count
            galaxies_seen += count
    return result
