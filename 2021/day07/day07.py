def part_a(raw_inp):
    inp = list(map(int, raw_inp.split(",")))
    return min(sum(abs(j - i) for j in inp) for i in range(min(inp), max(inp)+1))


def part_b(raw_inp):
    inp = list(map(int, raw_inp.split(",")))
    return min(sum(triangular(abs(j - i)) for j in inp) for i in range(min(inp), max(inp) + 1))


def triangular(n):
    return n*(n+1)//2
