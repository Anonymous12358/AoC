identifiableLengths = {2: 1, 3: 7, 4: 4, 7: 8}


def part_a(raw_inp):
    outputs = [line[line.index("|")+2:] for line in raw_inp.split("\n")]
    return sum(len(i) in identifiableLengths for line in outputs for i in line.split())


def solve_line(line):
    digits = [set(digit) for digit in line[:line.index(" |")].split()]
    ordered_digits = [None]*10
    for digit in digits:
        if len(digit) in identifiableLengths:
            ordered_digits[identifiableLengths[len(digit)]] = digit
    for digit in ordered_digits:
        if digit is not None:
            digits.remove(digit)

    # Segments for 9 are a superset of segments for 4
    ordered_digits[9] ,= tuple(digit for digit in digits if digit > ordered_digits[4])
    digits.remove(ordered_digits[9])
    # Segments for 6 aren't a superset of segments for 1, but other 6-segment numbers are
    ordered_digits[6] ,= tuple(digit for digit in digits if len(digit) == 6 and not digit > ordered_digits[1])
    digits.remove(ordered_digits[6])
    # 0 is the only remaining 6-segment number
    ordered_digits[0] ,= tuple(digit for digit in digits if len(digit) == 6)
    digits.remove(ordered_digits[0])
    # Segments for 3 are a superset of segments for 1, but other 5-segment numbers aren't
    ordered_digits[3] ,= tuple(digit for digit in digits if len(digit) == 5 and digit > ordered_digits[1])
    digits.remove(ordered_digits[3])
    # 5 is a subset of 6
    ordered_digits[5] ,= tuple(digit for digit in digits if digit < ordered_digits[6])
    digits.remove(ordered_digits[5])
    # Only 2 remains
    ordered_digits[2] = digits.pop()

    output = list(map(set, line[line.index("|")+2:].split()))
    return ordered_digits.index(output[0]) * 1000 + ordered_digits.index(output[1]) * 100 + ordered_digits.index(output[2]) * 10 + ordered_digits.index(output[3])


def part_b(inp):
    return sum(map(solve_line, inp))
