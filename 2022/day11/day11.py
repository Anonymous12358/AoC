import re
from collections import deque
from dataclasses import dataclass
from functools import reduce
from operator import add, mul
from typing import Callable

part = 0
pattern = re.compile(r'''Monkey (?P<index>\d+):
 {2}Starting items: (?P<items>(?:\d+, )*\d+)
 {2}Operation: new = old (?P<operator>[+*]) (?P<operand>\d+|old)
 {2}Test: divisible by (?P<divisor>\d+)
 {4}If true: throw to monkey (?P<true_target>\d+)
 {4}If false: throw to monkey (?P<false_target>\d+)''')


@dataclass
class Monkey:
    index: int
    items: deque[int]
    operator: Callable[[int, int], int]
    operand: int | None
    divisor: int
    targets: tuple[int, int]
    inspections: int = 0

    def give(self, item: int) -> None:
        self.items.append(item)

    def turn(self, monkeys: list['Monkey']) -> None:
        while self.items:
            item = self.items.popleft()
            item = self.operator(item, item if self.operand is None else self.operand)
            if part == 1:
                item //= 3
            elif part == 2:
                item %= 2 * 3 * 5 * 7 * 9 * 11 * 13 * 17 * 19
            target = self.targets[item % self.divisor == 0]
            monkeys[target].give(item)
            self.inspections += 1


def collect_monkeys(raw_inp) -> list[Monkey]:
    monkeys = []
    for monkey_str in raw_inp.split("\n\n"):
        index, items, operator, operand, divisor, true_target, false_target = re.match(pattern, monkey_str).groups()
        index = int(index)
        items = deque(map(int, items.split(", ")))
        operator = add if operator == "+" else mul
        operand = None if operand == "old" else int(operand)
        divisor = int(divisor)
        targets = int(false_target), int(true_target)
        monkeys.append(Monkey(index, items, operator, operand, divisor, targets))

    return monkeys


def solve(raw_inp):
    monkeys = collect_monkeys(raw_inp)
    for i in range(20 if part == 1 else 10_000):
        for monkey in monkeys:
            monkey.turn(monkeys)

    return reduce(mul, sorted(m.inspections for m in monkeys)[-2:])


def part_a(raw_inp):
    global part
    part = 1
    return solve(raw_inp)


def part_b(raw_inp):
    global part
    part = 2
    return solve(raw_inp)
