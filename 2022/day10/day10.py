DURATIONS = {"noop": 1, "addx": 2}


def part_a(inp):
    r"""
    /(\w{4})(?: (-?\d+))?/
    str int
    """
    registers = {"X": 1}
    # Initialise the clock to line up all of the sampling times to multiples of 40
    clock = -20
    total_strength = 0
    for instruction, arg in inp:
        clock += DURATIONS[instruction]
        # Check if we've passed a multiple of 40. We assume that no instruction lasts 40 or more cycles.
        if (clock - DURATIONS[instruction]) % 40 > clock % 40:
            total_strength += (clock // 40 * 40 + 20) * registers["X"]

        if instruction.startswith("add"):
            registers[instruction[-1].upper()] += arg

    return total_strength


def part_b(inp):
    r"""
    /(\w{4})(?: (-?\d+))?/
    str int
    """
    screen = ""
    # Collect the middles
    registers = {"X": 1}
    clock = 1
    for instruction, arg in inp:
        for _ in range(DURATIONS[instruction]):
            # For whatever reason, x positions on the CRT are measured from 0, while the clock starts from 1
            if abs((clock - 1) % 40 - registers["X"]) <= 1:
                # Doubling the width makes the screen much easier to read
                screen += "##"
            else:
                screen += ".."
            if clock % 40 == 0:
                screen += "\n"
            clock += 1

        if instruction.startswith("add"):
            registers[instruction[-1].upper()] += arg

    return screen
