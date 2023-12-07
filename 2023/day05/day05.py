def part_a(inp):
    """raw"""
    seeds = list(map(int, inp[7:inp.index("\n")].split()))
    maps = [[tuple(map(int, row.split())) for row in map_str.split("\n")[1:]] for map_str in inp.split("\n\n")[1:]]
    return min(convert_by_maps(maps, seed) for seed in seeds)


def convert_by_map(map_, value):
    for dest_start, source_start, length in map_:
        if source_start <= value < source_start + length:
            return dest_start + value - source_start
    return value


def convert_by_maps(maps, value):
    for map_ in maps:
        value = convert_by_map(map_, value)
    return value


def convert_range(map_, range_start, range_length):
    # Sort map - this will be useful later
    map_ = sorted(map_, key=lambda x: x[1])
    result = []
    for dest_start, source_start, map_length in map_:
        # Value range entirely included within source
        if source_start <= range_start < range_start + range_length <= source_start + map_length:
            result.append((dest_start + range_start - source_start, range_length))
            # Value range entirely consumed
            return result
        # Value range intersects end of source
        elif source_start <= range_start < source_start + map_length < range_start + range_length:
            result.append((dest_start + range_start - source_start, source_start + map_length - range_start))
            # Start of value range processed
            range_length = range_start + range_length - source_start - map_length
            range_start = source_start + map_length
        # Value range intersects start of source
        elif range_start <= source_start < range_start + range_length <= source_start + map_length:
            result.append((dest_start, range_start + range_length - source_start + dest_start))
            range_length = source_start - range_start
        # Value range entirely contains source
        elif range_start <= source_start < source_start + map_length <= range_start + range_length:
            # Since we sorted the source ranges by their starts, we know that everything before the start of the source
            # range is in no ranges, and can therefore be returned unchanged
            result.append((range_start, source_start - range_start))
            result.append((dest_start, map_length))
            range_length = range_start + range_length - source_start - map_length
            range_start = source_start + map_length
        # If value range and source do not overlap, then nothing needs to be done
        if range_length <= 0:
            break
    # Any value range leftover is not converted
    else:
        result.append((range_start, range_length))
    return result


def convert_ranges_by_maps(maps, ranges):
    for map_ in maps:
        # Ooh! It's a concatmap!
        ranges = [range_
                  for range_start, range_length in ranges
                  for range_ in convert_range(map_, range_start, range_length)]
    return ranges


def part_b(inp):
    """raw"""
    seeds = list(map(int, inp[7:inp.index("\n")].split()))
    # itertools.batched in python 3.11
    ranges = list(zip(*(iter(seeds),)*2))
    maps = [[tuple(map(int, row.split())) for row in map_str.split("\n")[1:]] for map_str in inp.split("\n\n")[1:]]
    converted = convert_ranges_by_maps(maps, ranges)
    return min(range_start for range_start, _ in converted)
