def part_a(inp):
    step_risks = [list(map(int, line)) for line in inp]

    x_len, y_len = len(step_risks[-1]), len(step_risks)
    neighbour_ds = {(0, 1), (1, 0), (0, -1), (-1, 0)}
    destination = (x_len-1, y_len-1)
    max_risk = 10 * (x_len + y_len)

    risks = [[max_risk]*x_len for _ in range(y_len)]
    risks[0][0] = 0
    unvisited = {(x, y) for x in range(x_len) for y in range(y_len) if x or y}  # `if x or y` drops (0, 0) from the set

    curr_x, curr_y = 0, 0
    i = 0
    while True:
        curr_risk = risks[curr_y][curr_x]
        if (curr_x, curr_y) == destination:
            return curr_risk
        for neighbour_d in neighbour_ds:
            nb_x, nb_y = curr_x + neighbour_d[0], curr_y + neighbour_d[1]
            if 0 <= nb_x < x_len and 0 <= nb_y < y_len and (nb_x, nb_y) in unvisited:
                risks[nb_y][nb_x] = min(risks[nb_y][nb_x], curr_risk + step_risks[nb_y][nb_x])

        curr_x, curr_y = min(unvisited, key=lambda point: risks[point[1]][point[0]])
        unvisited.remove((curr_x, curr_y))
        if (i := i + 1) % 100 == 0:
            print(i)


def part_b(inp):
    print("This one takes a couple of hours")
    int_inp = [list(map(int, line)) for line in inp]
    step_risks = [[((i - 1 + dx + dy) % 9) + 1 for dx in range(5) for i in row] for dy in range(5) for row in int_inp]
    return part_a(step_risks)
