from functools import reduce

digits = ["=", "-", "0", "1", "2"]
digit_sums = ["-0", "-1", "-2", "0=", "0-", "00", "01", "02", "1=", "1-", "10"]


def add_digits(a: str, b: str, cin: str) -> tuple[str, str]:
    value = digits.index(a) + digits.index(b) + digits.index(cin)
    return tuple(digit_sums[value - 1])


def add_snafus(a: str, b: str) -> str:
    result = []
    carry = "0"
    for a_digit, b_digit in zip(reversed(a), reversed(b)):
        carry, digit = add_digits(a_digit, b_digit, carry)
        result.append(digit)

    remainder = a[:-len(b)] if len(a) > len(b) else b[:-len(a)]
    for rem_digit in reversed(remainder):
        carry, digit = add_digits(rem_digit, "0", carry)
        result.append(digit)
    return "".join(reversed(result))


def part_a(inp):
    return reduce(add_snafus, inp)
