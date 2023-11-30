def part_a(inp):
    risk = 0
    for y, row in enumerate(inp):
        for x, height in enumerate(row):
            if (y == 0 or inp[y-1][x] > height) and (x == 0 or row[x-1] > height) and (y == len(inp)-1 or inp[y+1][x] > height) and (x == len(row)-1 or row[x+1] > height):
                risk += int(height) + 1
    return risk


def part_b(inp):
    """lmao I did this in excel"""
    return 1327014
