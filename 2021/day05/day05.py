import re
from collections import defaultdict


def part_a(inp):
    points = defaultdict(int)
    for line in inp:
        m = re.match("(\\d+),(\\d+) -> (\\d+),(\\d+)", line)
        x1, y1, x2, y2 = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))

        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2)+1):
                points[(x1, y)] += 1
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2)+1):
                points[(x, y1)] += 1
    return len(list(filter(lambda x: x > 1, points.values())))


def part_b(inp):
    points = defaultdict(int)
    for line in inp:
        m = re.match("(\\d+),(\\d+) -> (\\d+),(\\d+)", line)
        x1, y1, x2, y2 = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))

        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                points[(x1, y)] += 1
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                points[(x, y1)] += 1
        elif (x1 > x2) == (y1 > y2):
            for d in range(max(x1, x2) - min(x1, x2) + 1):
                points[(min(x1, x2) + d, min(y1, y2) + d)] += 1
        else:
            for d in range(max(x1, x2) - min(x1, x2) + 1):
                points[(min(x1, x2) + d, max(y1, y2) - d)] += 1

    return len(list(filter(lambda x: x > 1, points.values())))
