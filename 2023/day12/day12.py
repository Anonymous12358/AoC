import functools
import itertools


def replace_questions(iter1, iter2):
    for next_value in iter1:
        if next_value == "?":
            yield next(iter2)
        else:
            yield next_value


def count_runs(it):
    curr = 0
    for next_value in it:
        if next_value == "#":
            curr += 1
        elif curr > 0:
            yield curr
            curr = 0
    if curr > 0:
        yield curr


def part_a(inp):
    r"""
    /([.#?]+) ([\d,]+)/
    """
    result = 0
    for springs, runs in inp:
        runs = list(map(int, runs.split(",")))
        for replacements in itertools.product(*(".#",) * springs.count("?")):
            check = replace_questions(iter(springs), iter(replacements))
            if list(count_runs(check)) == runs:
                result += 1

    return result


def unfold_line(line):
    springs, runs = line
    return (springs + "?") * 4 + springs, (runs + ",") * 4 + runs


def part_b(inp):
    r"""
    /([.#?]+) ([\d,]+)/
    """
    result = 0
    for springs, runs in map(unfold_line, inp):
        runs = tuple(map(int, runs.split(",")))
        result += count_solutions(tuple(springs), tuple(runs))

    return result


@functools.cache
def count_solutions(springs: tuple[str], runs: tuple[int]) -> int:
    """This code has a bunch of overhead in Python because it was originally written in Haskell"""
    match springs:
        case ("?", *tail):
            return count_solutions(("#", *tail), runs) + count_solutions((".", *tail), runs)
        case ("#", "?", *tail):
            return count_solutions(("#", "#", *tail), runs) + count_solutions(("#", ".", *tail), runs)
        case (".", *tail):
            return count_solutions(tuple(tail), runs)
        case ("#", ".", *tail):
            return bool(runs) and runs[0] == 1 and count_solutions(tuple(tail), runs[1:])
        case ("#",):
            return runs == (1,)
        case ("#", *tail):
            return bool(runs) and runs[0] >= 2 and count_solutions(tuple(tail), (runs[0] - 1, *runs[1:]))
        case ():
            return not runs
        case _:
            return 0
