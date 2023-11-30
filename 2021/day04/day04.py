import numpy as np


def part_a(raw_inp):
    nums, boards = get_nums_and_boards(raw_inp)
    for num in nums:
        for board in boards:
            board[board == num] = 0
            if is_winning(board):
                return board.sum() * num


def part_b(raw_inp):
    nums, boards = get_nums_and_boards(raw_inp)
    for num in nums:
        for i, board in enumerate(boards):
            board[board == num] = 0
            if is_winning(board):
                # When the last board wins, return immediately
                if len(boards) == 1:
                    return boards[0].sum() * num
                # Otherwise, remove the board
                boards[i] = None  # Set to None and remove at end of loop to avoid messing up the boards list
        boards = list(filter(lambda x: x is not None, boards))


def get_nums_and_boards(raw_inp):
    # Replacing 0 with -1 allows us to use 0 to denote a crossed-off number, which makes the rest of the code much nicer
    nums = map(lambda x: int(x) or -1, raw_inp[:raw_inp.index("\n")].split(","))
    boards = [np.array(list(map(lambda x: int(x) or -1, board.split()))).reshape(5, 5) for board in
              raw_inp.split("\n\n")[1:]]
    return nums, boards


def is_winning(board):
    return any(row.sum() == 0 for row in board) or any(col.sum() == 0 for col in board.T)
