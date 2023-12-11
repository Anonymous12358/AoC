def part_a(inp):
    """
    split " "
    int
    """
    result = 0
    for line in inp:
        derivatives = [line]
        while any(term != 0 for term in derivatives[-1]):
            derivatives.append([derivatives[-1][i] - derivatives[-1][i-1] for i in range(1, len(derivatives[-1]))])
        result += sum(line[-1] for line in derivatives)
    return result


def part_b(inp):
    """
    split " "
    int
    """
    result = 0
    for line in inp:
        derivatives = [line]
        while any(term != 0 for term in derivatives[-1]):
            derivatives.append([derivatives[-1][i] - derivatives[-1][i-1] for i in range(1, len(derivatives[-1]))])
        result += sum((-1) ** i * line[0] for i, line in enumerate(derivatives))
    return result
