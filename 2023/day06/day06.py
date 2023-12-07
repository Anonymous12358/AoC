import math


def part_a(inp):
    r"""
    /\w+: *([\d ]+)/
    """
    # For a given race length t ms, holding the button for x ms gives a distance of
    # x * (t-x) mm = -x^2 + tx mm
    # For a given distance s mm to beat, we need
    # -x^2 + tx - s > 0
    # -(x-(t/2))^2 - s + t^2/4 > 0
    # -(x-(t/2))^2 > s - t^2/4
    # (x-(t/2))^2 < t^2/4 - s
    # -sqrt(t^2/4 - s) < x-(t/2) < sqrt(t^2/4 - s)
    # -sqrt(t^2/4 - s) + t/2 < x < sqrt(t^2/4 - s) + t/2
    (times,), (distances,) = inp
    result = 1
    for time, distance in zip(map(int, times.split()), map(int, distances.split())):
        min_x = -math.sqrt(time ** 2 / 4 - distance) + time / 2
        max_x = math.sqrt(time ** 2 / 4 - distance) + time / 2
        result *= (math.ceil(max_x) - 1) - (math.floor(min_x) + 1) + 1
    return result


def part_b(inp):
    r"""
    /\w+: *([\d ]+)/
    """
    return part_a([(line[0].replace(" ", ""),) for line in inp])
