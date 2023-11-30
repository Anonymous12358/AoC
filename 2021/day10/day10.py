def part_a(inp):
    score = 0
    scores = {")": 3, "]": 57, "}": 1197, ">": 25137}
    closes = {")": "(", "]": "[", "}": "{", ">": "<"}
    for line in inp:
        stack = []
        for char in line:
            if char in closes:
                if stack.pop() != closes[char]:
                    score += scores[char]
                    break
            else:
                stack.append(char)

    return score


def part_b(inp):
    line_scores = []
    scores = {"(": 1, "[": 2, "{": 3, "<": 4}
    closes = {")": "(", "]": "[", "}": "{", ">": "<"}
    for line in inp:
        stack = []
        for char in line:
            if char in closes:
                if stack.pop() != closes[char]:
                    break
            else:
                stack.append(char)
        else:
            score = 0
            while stack:
                score *= 5
                score += scores[stack.pop()]
            line_scores.append(score)
    return sorted(line_scores)[len(line_scores)//2]
