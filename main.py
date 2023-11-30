import importlib
import itertools
import os
from inspect import signature
import pydoc
import re

import numpy as np

YEAR = 2022


def main():
    challenge = input("Enter challenge number: ").split()
    print(solve_challenge(challenge[0], challenge[1], *challenge[2:]))


def solve_challenge(day, part, inp_name="inp"):
    # Get the code for the solution
    try:
        solution = importlib.import_module(f"{YEAR}.day{day}.day{day}{part}").main
    except ImportError:
        solution = getattr(importlib.import_module(f"{YEAR}.day{day}.day{day}"), "part_" + part)

    # Some manipulation to get the input file from inside a folder
    script_dir = os.path.dirname(__file__)
    inp_path = f"{script_dir}/{YEAR}/day{day}/{inp_name}.txt"
    with open(inp_path, "r") as inp_file:
        raw_inp = inp_file.read()

    # Four modes: raw, split lines (default), cast to np array, and quick array (default way AoC does grids)
    if solution.__doc__:
        mode = solution.__doc__.partition("\n")[0] or "split"
    elif "raw_inp" in signature(solution).parameters:
        mode = "raw"
    else:
        mode = "split"

    if mode == "raw":
        if solution.__doc__:
            inp = pre_process(raw_inp, **parse_doc(solution.__doc__))
        else:
            inp = raw_inp
    elif mode == "array":
        if solution.__doc__:
            inp = np.array([pre_process(line, **parse_doc(solution.__doc__)) for line in raw_inp.splitlines()])
        else:
            inp = np.array(list(map(list, raw_inp.splitlines())))
    elif mode == "quick array":
        inp = np.array([pre_process(line, **parse_doc("array\nsplit\nbool\n.#\n")) for line in raw_inp.splitlines()])
    elif mode == "split":
        if solution.__doc__:
            inp = [pre_process(line, **parse_doc(solution.__doc__)) for line in raw_inp.splitlines()]
        else:
            inp = raw_inp.splitlines()
    else:
        raise ValueError(f"Invalid mode: {mode}")

    return solution(inp)


def parse_doc(doc: str) -> dict[str, str]:
    kwargs = {}
    lines = doc.split("\n")
    if len(lines) >= 3:
        kwargs['pattern'] = lines[1].lstrip()
    if len(lines) >= 4:
        kwargs['types'] = lines[2].lstrip()
    if len(lines) >= 5:
        kwargs['palettes'] = lines[3].lstrip()

    return kwargs


def pre_process(inp: str, **kwargs: str) -> tuple:
    if 'pattern' not in kwargs or kwargs['pattern'] == 'keep':
        groups = (inp,)
    elif kwargs['pattern'][0] == kwargs['pattern'][-1] == '/':
        groups = re.match(kwargs['pattern'][1:-1], inp).groups()
    elif kwargs['pattern'].startswith('split "') and kwargs['pattern'].endswith('"'):
        groups = inp.split(kwargs['pattern'][7:-1])
    elif kwargs['pattern'] == 'split':
        groups = inp
    else:
        raise ValueError(f"Invalid pattern: {kwargs['pattern']}")

    if 'types' in kwargs:
        types = itertools.cycle(map(pydoc.locate, kwargs['types'].split(" ")))
    else:
        types = itertools.cycle((str,))
    if 'palettes' in kwargs:
        palettes = itertools.cycle(dict(map(reversed, enumerate(palette))) for palette in kwargs['palettes'].split())
    else:
        palettes = itertools.cycle(('',))

    processed_groups = []
    for group, type_, palette in zip(groups, types, palettes):
        if group is None:
            # Groups that don't match should pass through gracefully, even if None can't be cast to the type
            processed_groups.append(None)
        elif issubclass(type_, int) and palette:
            processed_groups.append(type_(palette[group]))
        else:
            processed_groups.append(type_(group))

    if 'pattern' not in kwargs or kwargs['pattern'] == 'keep':
        return processed_groups[0]
    else:
        return tuple(processed_groups)


if __name__ == '__main__':
    main()
