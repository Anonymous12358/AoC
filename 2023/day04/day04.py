def part_a(inp):
    r"""
    /Card [ \d]+:([ \d]+)\|([ \d]+)/
    """
    result = 0
    for winning, have in inp:
        winning_count = len(set(winning.split()) & set(have.split()))
        if winning_count > 0:
            result += 1 << (winning_count - 1)
    return result


def part_b(inp):
    r"""
    /Card [ \d]+:([ \d]+)\|([ \d]+)/
    """
    instances = {i: 1 for i in range(len(inp))}
    for i, (winning, have) in enumerate(inp):
        winning_count = len(set(winning.split()) & set(have.split()))
        for j in range(i + 1, i + winning_count + 1):
            instances[j] += instances[i]
    return sum(instances.values())
