from operator import add, mul, mod, eq
from math import trunc

OPERATIONS = {
    "add": add,
    "mul": mul,
    "div": lambda a, b: trunc(a/b),  # Unfortunately, Python's floordiv always rounds down, while we want to truncate
    "mod": mod,
    "eql": eq
}


def part_a(inp):
    #                 0123456789abcd
    model = map(int, "00000200100100")

    regs = {"w": 0, "x": 0, "y": 0, "z": 0}
    for line in inp:
        opcode, args = line.split()[0], line.split()[1:]
        if opcode == "inp":
            regs[args[0]] = next(model)
        else:
            regs[args[0]] = OPERATIONS[opcode](regs[args[0]], regs[args[1]] if args[1] in regs else int(args[1]))
    return regs
