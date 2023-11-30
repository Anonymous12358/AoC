def part_a(inp):
    horizontal, depth = 0, 0
    for line in inp:
        match line[0]:
            case "f":
                horizontal += int(line[8:])
            case "d":
                depth += int(line[5:])
            case "u":
                depth -= int(line[3:])
    return horizontal * depth


def part_b(inp):
    horizontal, depth, aim = 0, 0, 0
    for line in inp:
        match line[0]:
            case "f":
                horizontal += int(line[8:])
                depth += int(line[8:]) * aim
            case "d":
                aim += int(line[5:])
            case "u":
                aim -= int(line[3:])
    return horizontal * depth
