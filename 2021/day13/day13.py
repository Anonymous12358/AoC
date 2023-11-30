def do_fold(points, position, dimension):
    new_points = set()
    for point in points:
        if point[dimension] > position:
            new_points.add(point[:dimension] + (position * 2 - point[dimension],) + point[dimension+1:])
        else:
            new_points.add(point)
    return new_points


def process_inp(inp):
    letter_to_dimension = {"x": 0, "y": 1}
    points = {tuple(map(int, line.split(","))) for line in inp[:inp.index("")]}
    folds = [(int(line[13:]), letter_to_dimension[line[11]]) for line in inp[inp.index("")+1:]]
    return points, folds


def part_a(inp):
    points, folds = process_inp(inp)
    return len(do_fold(points, *folds[0]))


def part_b(inp):
    points, folds = process_inp(inp)
    for fold in folds:
        points = do_fold(points, *fold)

    for y in range(max(point[1] for point in points) + 1):
        for x in range(max(point[0] for point in points) + 1):
            if (x, y) in points:
                print("██", end="")
            else:
                print("  ", end="")
        print()
    return "Look at the printed string to see the code"
