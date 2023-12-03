import re


def part_a(inp):
    max_cubes = {"red": 12, "green": 13, "blue": 14}
    result = 0
    for i, line in enumerate(inp):
        for show in re.split("[;,] ", line.partition(": ")[2]):
            num, _, color = show.partition(" ")
            color = color.removesuffix(";").removesuffix(",")
            if int(num) > max_cubes[color]:
                break
        else:
            result += i + 1
    return result


def part_b(inp):
    result = 0
    for i, line in enumerate(inp):
        min_cubes = {"red": 0, "blue": 0, "green": 0}
        for show in re.split("[;,] ", line.partition(": ")[2]):
            num, _, color = show.partition(" ")
            min_cubes[color] = max(min_cubes[color], int(num))
        result += min_cubes["red"] * min_cubes["green"] * min_cubes["blue"]
    return result
