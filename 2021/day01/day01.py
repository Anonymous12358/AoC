def part_a(inp):
    inp = list(map(int, inp))
    return sum(inp[i] > inp[i-1] for i in range(1, len(inp)))


def part_b(inp):
    inp = list(map(int, inp))
    return sum(inp[i] > inp[i - 3] for i in range(3, len(inp)))
