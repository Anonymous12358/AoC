def mix_list(lst: list[int], mixes: int = 1) -> list[int]:
    mixed = list(zip(lst, range(len(lst))))

    for _ in range(mixes):
        for num, orig_index in zip(lst, range(len(lst))):
            idx = mixed.index((num, orig_index))
            mixed.pop(idx)
            mixed.insert((idx + num) % len(mixed), (num, orig_index))

    return [num for num, _ in mixed]


def part_a(inp):
    """
    keep
    int
    """
    mixed = mix_list(inp)
    idx = mixed.index(0)
    return sum(mixed[(idx + 1000 * i) % len(mixed)] for i in range(1, 4))


def part_b(inp):
    """
    keep
    int
    """
    mixed = mix_list([811589153 * line for line in inp], 10)
    idx = mixed.index(0)
    return sum(mixed[(idx + 1000 * i) % len(mixed)] for i in range(1, 4))
