from functools import partial
import re


def part_a(raw_inp):
    return solve(raw_inp, 1)


def part_b(raw_inp):
    return solve(raw_inp, 2)


def solve(raw_inp, part):
    # Separate input into boxes and instructions
    boxes_strs, _, procedure = map(partial(str.split, sep="\n"), raw_inp.partition("\n\n"))

    # Get the boxes
    # Look at the labels to find out how many columns there are
    boxes = [[] for _ in range((len(boxes_strs[-1]) + 2) // 4)]
    for line in boxes_strs[-1::-1]:
        for i, char in enumerate(line[1::4]):
            if char != " ":
                boxes[i].append(char)

    # Perform the procedure
    for line in procedure:
        count, src, dest = map(int, re.match(r"move (\d+) from (\d+) to (\d+)", line).groups())
        # Grab a slice from one stack, copy it to the other, then delete it from the source
        # [::(-3+2*part)] reverses the stack iff we're doing part a
        boxes[dest-1] += boxes[src-1][-count:][::(-3+2*part)]
        del boxes[src-1][-count:]

    return "".join(stack[-1] for stack in boxes)
