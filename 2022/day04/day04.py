def part_a(inp):
    r"""
    /(\d+)-(\d+),(\d+)-(\d+)/
    int
    """
    # Check if the extremes of one range are both within the other
    return sum(a <= c <= d <= b or c <= a <= b <= d for a, b, c, d in inp)


def part_b(inp):
    r"""
    /(\d+)-(\d+),(\d+)-(\d+)/
    int
    """
    # Either first range contains one of the ends of the second, or second range entirely contains the first
    return sum(a <= d <= b or a <= c <= b or c <= a <= d for a, b, c, d in inp)
