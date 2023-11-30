import re


def do_it(raw_inp):
    m = re.match("target area: x=(-?\\d+)..(-?\\d+), y=(-?\\d+)..(-?\\d+)", raw_inp)
    x_min, x_max, y_min, y_max = tuple(int(m.group(i)) for i in range(1, 5))

    best, hits = 0, 0
    for dx_i in range(200):
        for dy_i in range(-200, 300):
            dx, dy = dx_i, dy_i
            x, y = 0, 0
            peak = 0
            while x <= x_max and y_min <= y:
                if x_min <= x and y <= y_max:
                    best = max(best, peak)
                    hits += 1
                    break

                x += dx
                y += dy
                if dx:
                    dx -= 1
                dy -= 1
                if y > peak:
                    peak = y
    return best, hits


def part_a(raw_inp):
    return do_it(raw_inp)[0]


def part_b(raw_inp):
    return do_it(raw_inp)[1]
