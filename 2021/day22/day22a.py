import re


def parse_inp(inp):
    pattern = re.compile(r"\w+=(-?\d+)\.\.(-?\d+)")
    steps = []
    for line in inp:
        mode = line.split()[0] == "on"
        coords = []
        for ordinate in line.split()[1].split(","):
            m = re.match(pattern, ordinate)
            if abs(int(m.group(1))) > 50:  # Stop when things leave the initialisation procedure range
                return steps[::-1]  # Reverse here since we want to iterate backwards - later steps take precedence
            coords.append((int(m.group(1)), int(m.group(2))))
        steps.append((mode, tuple(coords)))

    return steps[::-1]


def is_on(coords, steps):
    for step in steps:
        if all(step_ordinate[0] <= ordinate <= step_ordinate[1] for ordinate, step_ordinate in zip(coords, step[1])):
            return step[0]
    return False


def main(inp):
    steps = parse_inp(inp)
    return sum(is_on((x, y, z), steps) for x in range(-50, 51) for y in range(-50, 51) for z in range(-50, 51))
