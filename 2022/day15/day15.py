def get_ranges(coords, target_y):
    # Find the ranges invalidated by each sensor
    ranges = set()
    for sensor_x, sensor_y, beacon_x, beacon_y in coords:
        distance = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
        # The amount by which we can spread out once we reach the target y
        spread = distance - abs(sensor_y - target_y)
        if spread < 0:
            continue

        # The range invalidated by the current sensor
        start, end = sensor_x - spread, sensor_x + spread
        # Intersect the new range with existing ranges
        for other_start, other_end in set(ranges):
            if other_start <= start <= end <= other_end:
                # The new range is entirely contained within another, so contributes nothing
                break
            elif start <= other_start <= other_end <= end:
                # The other range is entirely contained within the new, so delete it entirely
                ranges.remove((other_start, other_end))
            elif other_start <= start <= other_end <= end:
                # Partial intersection - combine the two ranges, replacing the old one
                ranges.remove((other_start, other_end))
                start = other_start
            elif start <= other_start <= end <= other_end:
                # Partial intersection
                ranges.remove((other_start, other_end))
                end = other_end
        else:
            ranges.add((start, end))

    return ranges


def part_a(inp):
    r"""
    /Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)/
    int
    """
    ranges = get_ranges(inp, 2_000_000)

    # The invalidated ranges can't contain unknown beacons, but they may still contain known ones
    beacons_on_target_y = {x for _, _, x, y in inp if y == 2_000_000}
    total = 0
    for start, end in ranges:
        total += end - start + 1
        total -= sum(start <= beacon <= end for beacon in beacons_on_target_y)
    return total


def part_b(inp):
    r"""
    /Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)/
    int
    """
    for target_y in range(4_000_000):
        ranges = get_ranges(inp, target_y)
        if not any(start <= 0 and 4_000_000 <= end for start, end in ranges):
            target_x = max(end for _, end in ranges if end <= 4_000_000) + 1
            return 4_000_000 * target_x + target_y
