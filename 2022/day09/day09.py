DIRECTIONS = {"U": (1, 0), "D": (-1, 0), "L": (0, -1), "R": (0, 1)}


def sgn(n):
    return (n > 0) - (n < 0)


def part_a(inp):
    r"""
    /(\w) (\d+)/
    str int
    """
    head, tail = (0, 0), (0, 0)
    visited = {(0, 0)}
    for direction, amount in inp:
        delta = DIRECTIONS[direction]
        for _ in range(amount):
            head = tuple(map(sum, zip(head, delta)))
            if any(abs(head_ord - tail_ord) > 1 for tail_ord, head_ord in zip(tail, head)):
                tail = tuple(tail_ord + sgn(head_ord - tail_ord) for tail_ord, head_ord in zip(tail, head))
            visited.add(tail)

    return len(visited)


def part_b(inp):
    r"""
    /(\w) (\d+)/
    str int
    """
    knots = [(0, 0)]*10
    visited = {(0, 0)}
    for direction, amount in inp:
        delta = DIRECTIONS[direction]
        for _ in range(amount):
            knots[0] = tuple(map(sum, zip(knots[0], delta)))
            for i in range(len(knots) - 1):
                if any(abs(head_ord - tail_ord) > 1 for tail_ord, head_ord in zip(knots[i+1], knots[i])):
                    knots[i+1] = tuple(tail_ord + sgn(head_ord - tail_ord)
                                       for tail_ord, head_ord in zip(knots[i+1], knots[i]))
                else:
                    break
            visited.add(knots[-1])

    return len(visited)
