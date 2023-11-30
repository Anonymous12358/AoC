import re
from collections.abc import Iterable
import operator

import numpy as np

PATH, WALL, PORTAL = range(3)


def add(*iterables: Iterable) -> tuple:
    return tuple(map(sum, zip(*iterables)))


def check_bounds(board: np.ndarray, coords: tuple[int, ...]) -> bool:
    return all(0 <= ordinate < length for ordinate, length in zip(coords, board.shape))


def move_a(board: np.ndarray, coords: tuple[int, ...], delta: tuple[int, ...], distance: int) -> tuple[int, ...]:
    for _ in range(distance):
        prev = coords
        coords = tuple(map(sum, zip(coords, delta)))

        if not check_bounds(board, coords) or board[coords] == PORTAL:
            # Move backwards until we hit a portal, then move forwards one
            coords = add(coords, map(operator.neg, delta))
            while check_bounds(board, coords) and board[coords] != PORTAL:
                coords = add(coords, map(operator.neg, delta))
            coords = add(coords, delta)

        if board[coords] == WALL:
            # Undo this step, even if it included a portal
            coords = prev
            break

    return coords


def move_b(board: np.ndarray, coords: tuple[int, int], delta: tuple[int, int], distance: int
           ) -> tuple[tuple[int, int], tuple[int, int]]:
    for _ in range(distance):
        prev = coords, delta
        coords = tuple(map(sum, zip(coords, delta)))

        if not check_bounds(board, coords) or board[coords] == PORTAL:
            y, x = coords
            # Box 1, left -> box 4, left
            if 0 <= y < 50 and x == 49:
                coords = 149 - y, 0
                delta = 0, 1
            # Box 1, top -> box 6, left
            elif y == -1 and 50 <= x < 100:
                coords = x + 100, 0
                delta = 0, 1
            # Box 2, top -> box 6, bottom
            elif y == -1 and 100 <= x < 150:
                coords = 199, x - 100
                delta = -1, 0
            # Box 2, right -> box 5, right
            elif 0 <= y < 50 and x == 150:
                coords = 149 - y, 99
                delta = 0, -1
            # Box 1, left <- box 4, left
            elif 100 <= y < 150 and x == -1:
                coords = 149 - y, 50
                delta = 0, 1
            # Box 1, top <- box 6, left
            elif 150 <= y < 200 and x == -1:
                coords = 0, y - 100
                delta = 1, 0
            # Box 2, top <- box 6, bottom
            elif y == 200 and 0 <= x < 50:
                coords = 0, x + 100
                delta = 1, 0
            # Box 2, right <- box 5, right
            elif 100 <= y < 150 and x == 100:
                coords = 149 - y, 149
                delta = 0, -1
            # Box 2, bottom -> box 3, right
            elif y == 50 and 100 <= x < 150 and delta == (1, 0):
                coords = x - 50, 99
                delta = 0, -1
            # Box 2, bottom <- box 3, right
            elif 50 <= y < 100 and x == 100 and delta == (0, 1):
                coords = 49, y + 50
                delta = -1, 0
            # Box 3, left -> box 4, top
            elif 50 <= y < 100 and x == 49 and delta == (0, -1):
                coords = 100, y - 50
                delta = 1, 0
            # Box 3, left <- box 4, top
            elif y == 99 and 0 <= x < 50 and delta == (-1, 0):
                coords = x + 50, 50
                delta = 0, 1
            # Box 5, bottom -> box 6, right
            elif y == 150 and 50 <= x < 100 and delta == (1, 0):
                coords = x + 100, 49
                delta = 0, -1
            # Box 5, bottom <- box 6, right
            elif 150 <= y < 200 and x == 50 and delta == (0, 1):
                coords = 149, y - 100
                delta = -1, 0

        if board[coords] == WALL:
            # Undo this step, even if it included a portal
            coords, delta = prev
            break

    return coords, delta


def part_a(raw_inp):
    board_str, instructions = raw_inp.split("\n\n")
    board_strs = board_str.split("\n")
    for i, line in enumerate(board_strs):
        board_strs[i] = line + " " * (max(map(len, board_strs)) - len(line))
    board = np.array(list(map(list, board_strs)))
    board = PATH * (board == ".") + WALL * (board == "#") + PORTAL * (board == " ")

    coords = 0, next(i for i, value in enumerate(board[0]) if value == PATH)
    delta = 0, 1
    for instruction in re.split(r'(?<=\d)(?=\D)|(?<=\D)(?=\d)', instructions):
        if instruction.isdigit():
            coords = move_a(board, coords, delta, int(instruction))
        elif instruction == "R":
            delta = delta[1], -delta[0]
        elif instruction == "L":
            delta = -delta[1], delta[0]

    return 1004 + 1000 * coords[0] + 4 * coords[1] + [(0, 1), (1, 0), (0, -1), (-1, 0)].index(delta)


def part_b(raw_inp):
    board_str, instructions = raw_inp.split("\n\n")
    board_strs = board_str.split("\n")
    for i, line in enumerate(board_strs):
        board_strs[i] = line + " " * (max(map(len, board_strs)) - len(line))
    board = np.array(list(map(list, board_strs)))
    board = PATH * (board == ".") + WALL * (board == "#") + PORTAL * (board == " ")

    coords = 0, next(i for i, value in enumerate(board[0]) if value == PATH)
    delta = 0, 1
    for instruction in re.split(r'(?<=\d)(?=\D)|(?<=\D)(?=\d)', instructions):
        print(instruction, coords, delta)
        if instruction.isdigit():
            coords, delta = move_b(board, coords, delta, int(instruction))
        elif instruction == "R":
            delta = delta[1], -delta[0]
        elif instruction == "L":
            delta = -delta[1], delta[0]

    return 1004 + 1000 * coords[0] + 4 * coords[1] + [(0, 1), (1, 0), (0, -1), (-1, 0)].index(delta)
