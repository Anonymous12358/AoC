import functools
import itertools
import math
import re


def part_a(inp):
    instructions = inp[0]
    graph = {}
    for node_str in inp[2:]:
        m = re.match(r"(\w{3}) = \((\w{3}), (\w{3})\)", node_str)
        graph[m.group(1)] = (m.group(2), m.group(3))

    pos = "AAA"
    i = -1
    for i, instr in enumerate(itertools.cycle(instructions)):
        pos = graph[pos]["LR".index(instr)]
        if pos == "ZZZ":
            break
    return i + 1


def part_b(inp):
    instructions = inp[0]
    graph = {}
    for node_str in inp[2:]:
        m = re.match(r"(\w{3}) = \((\w{3}), (\w{3})\)", node_str)
        graph[m.group(1)] = (m.group(2), m.group(3))

    periods = set()
    for pos in graph.keys():
        if pos[2] != "A":
            continue
        seen = [(pos, 0)]
        for i, (j, instr) in enumerate(itertools.cycle(enumerate(instructions))):
            pos = graph[pos]["LR".index(instr)]
            if pos[2] == "Z":
                # print(f"{seen[0][0]} reaches {pos} after {i+1} iterations")
                periods.add(i+1)
            if (pos, j) in seen:
                # print(f"{seen[0][0]} cycles after {i+1} iterations; first hit {pos, j} after {seen.index((pos, j))}")
                break
            seen.append((pos, j))

    # We can see from the printouts that it just so happens that all of the paths reach their end after an integer
    # number of their own cycles
    return functools.reduce(math.lcm, periods)
