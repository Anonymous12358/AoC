import operator
import re

import sympy

OPERATIONS = {"+": operator.add, "-": operator.sub, "*": operator.mul, "/": operator.truediv}


def part_a(inp):
    r"""
    /(\w{4}): (.+)/
    """
    monkeys = dict(inp)
    while isinstance(monkeys["root"], str):
        for name, yell in monkeys.items():
            if not isinstance(yell, str):
                continue
            if yell.isdigit():
                monkeys[name] = int(yell)
            else:
                operand1, operation, operand2 = re.match(r'(\w{4}) ([-+*/]) (\w{4})', yell).groups()
                if not isinstance(monkeys[operand1], str) and not isinstance(monkeys[operand2], str):
                    monkeys[name] = OPERATIONS[operation](monkeys[operand1], monkeys[operand2])

    return int(monkeys["root"])


def part_b(inp):
    r"""
    /(\w{4}): (.+)/
    """
    monkeys = dict(inp)
    monkeys["humn"] = sympy.Symbol("x")

    while isinstance(monkeys["gqjg"], str) or isinstance(monkeys["rpjv"], str):
        for name, yell in monkeys.items():
            if not isinstance(yell, str):
                continue
            if yell.isdigit():
                monkeys[name] = int(yell)
            else:
                operand1, operation, operand2 = re.match(r'(\w{4}) ([-+*/]) (\w{4})', yell).groups()
                if not isinstance(monkeys[operand1], str) and not isinstance(monkeys[operand2], str):
                    monkeys[name] = OPERATIONS[operation](monkeys[operand1], monkeys[operand2])

    return int(sympy.solve(monkeys["gqjg"] - monkeys["rpjv"])[0])
