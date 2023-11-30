import itertools

import numpy as np


def add(*tuples: tuple) -> tuple:
    return tuple(map(sum, zip(*tuples)))


def step(elves: set[tuple[int, ...]], deltas: list[tuple[int, ...]]) -> set[tuple[int, ...]]:
    proposals = {}
    for elf in elves:
        if not elves & {add(elf, adj) for adj in itertools.product(*(range(-1, 2),) * len(elf)) if any(adj)}:
            proposals[elf] = elf
            continue

        for delta in deltas:
            dimension = next(i for i, ordinate in enumerate(delta) if ordinate)
            consider = set()
            for adjustment in itertools.product(*(range(-1, 2),) * (len(elf) - 1)):
                consider.add(add(elf, delta, adjustment[:dimension] + (0,) + adjustment[dimension:]))
            if not consider & elves:
                proposals[elf] = add(elf, delta)
                break
        else:
            # This case doesn't appear to be described in the problem, so this is my best guess of what should happen
            proposals[elf] = elf

    result = set()
    for elf, proposal in proposals.items():
        result.add(proposal if list(proposals.values()).count(proposal) == 1 else elf)
    return result


def simulate(elves: set[tuple[int, ...]], deltas: list[tuple[int, ...]], steps: int) -> set[tuple[int, ...]]:
    deltas = list(deltas)
    for _ in range(steps):
        elves = step(elves, deltas)
        deltas.append(deltas.pop(0))
    return elves


def find_ground(elves: set[tuple[int, ...]]) -> int:
    total = 1
    for dimension in range(len(next(iter(elves)))):
        total *= max(elf[dimension] for elf in elves) - min(elf[dimension] for elf in elves) + 1
    return total - len(elves)


def part_a(inp):
    """quick array"""
    elves = set(zip(*np.where(inp)))
    return find_ground(simulate(elves, [(-1, 0), (1, 0), (0, -1), (0, 1)], 10))


def part_b(inp):
    """quick array"""
    elves = set(zip(*np.where(inp)))
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    i = 0
    while True:
        new = step(elves, deltas)
        if new == elves:
            break
        elves = new
        deltas.append(deltas.pop(0))
        i += 1
    return i + 1
