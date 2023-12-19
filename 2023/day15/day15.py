import collections


def holiday_hash(s):
    result = 0
    for char in s:
        result = (result + ord(char)) * 17 % 256
    return result


def part_a(inp):
    """raw
    split ","
    """
    return sum(map(holiday_hash, inp))


def part_b(inp):
    """raw
    split ","
    """
    boxes = [collections.OrderedDict() for _ in range(256)]
    for instr in inp:
        if "-" in instr:
            label = instr[:-1]
            box = boxes[holiday_hash(label)]
            if label in box.keys():
                del box[label]
        else:
            label, _, focal_length = instr.partition("=")
            box = boxes[holiday_hash(label)]
            box[label] = focal_length

    return sum(
        sum(
            int(length) * (1 + j)
            for j, length in enumerate(box.values())
        ) * (1 + i) for i, box in enumerate(boxes)
    )
