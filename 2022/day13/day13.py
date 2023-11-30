from functools import cmp_to_key


def compare(left: int | list, right: int | list) -> int:
    """
    Compare two elements of packet data. Note the return format, which is chosen to work with functools.cmp_to_key.
    :param left: The values to compare
    :param right: The values to compare
    :return: -1 if the values are in order, 1 if they are not, or 0 if an order cannot be determined
    """
    # Both are integers
    if isinstance(left, int) and isinstance(right, int):
        return (left > right) - (left < right)

    # Precisely one is an integer - convert to list
    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]

    # Compare elementwise
    for left_element, right_element in zip(left, right):
        result = compare(left_element, right_element)
        if result:
            return result

    # Compare lengths
    return (len(left) > len(right)) - (len(left) < len(right))


def part_a(raw_inp):
    packets = [tuple(map(eval, pair.split("\n"))) for pair in raw_inp.split("\n\n")]
    total = sum(i + 1 for i, (left_packet, right_packet) in enumerate(packets)
                if compare(left_packet, right_packet) == -1)
    return total


def part_b(inp):
    packets = [[[2]], [[6]]] + [eval(line) for line in inp if line != ""]
    sorted_packets = sorted(packets, key=cmp_to_key(compare))
    return (sorted_packets.index([[2]]) + 1) * (sorted_packets.index([[6]]) + 1)
