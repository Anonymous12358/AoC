import re


def part_a(raw_inp):
    return len(re.match(r'^(.*?)(.)(?!\2)(.)(?!\2|\3)(.)(?!\2|\3|\4)(.)', raw_inp).group(1)) + 4


def part_b(raw_inp):
    for start in range(len(raw_inp) - 14):
        if len(set(raw_inp[start:start+14])) == 14:
            return start + 14
