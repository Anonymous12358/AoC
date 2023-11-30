import numpy as np
from functools import wraps


def count_calls(func):
    """Counts the number of times a function is called"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.call_count += 1
        return func(*args, **kwargs)
    wrapper.call_count = 0
    return wrapper


@count_calls
def flash(array, coords):
    array[tuple(slice(max(ordinate-1, 0), ordinate+2) for ordinate in coords)] += 1
    array[coords] = -128  # Set the octopus that just flashed to -128 so it won't flash again this step


@count_calls
def step(array):
    array[...] += 1
    while (array > 9).any():
        for coords in zip(*np.where(array > 9)):  # np.where has a weird return format. zip(*iterable) rotates it to our needs
            flash(array, coords)
    array[array < 0] = 0


def part_a(inp):
    flash.call_count = 0
    array = np.array([list(map(int, line)) for line in inp], dtype=np.int8)
    for _ in range(100):
        step(array)
    return flash.call_count


def part_b(inp):
    step.call_count = 0
    array = np.array([list(map(int, line)) for line in inp], dtype=np.int8)
    while True:
        step(array)
        if (array == 0).all():
            return step.call_count
