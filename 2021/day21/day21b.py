from collections import defaultdict

POSITION, SCORE = range(2)
distribution = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}


def tuple_repl(tpl, value, index):
    return tpl[:index] + (value,) + tpl[index+1:]


def game(starts):
    states = {(starts, (0,) * len(starts)): 1}
    wins = [0] * len(starts)
    while states:
        for i in range(len(starts)):
            new_states = defaultdict(int)
            for state in states:
                for roll in distribution:
                    position = (state[POSITION][i] + roll - 1) % 10 + 1
                    score = state[SCORE][i] + position
                    occurrences = distribution[roll] * states[state]
                    if score >= 21:
                        wins[i] += occurrences
                        continue
                    new_states[tuple_repl(state[POSITION], position, i), tuple_repl(state[SCORE], score, i)] += occurrences
            states = new_states

    return wins


def parse_inp(inp):
    return tuple(int(line[28:]) for line in inp)


def main(inp):
    return max(game(parse_inp(inp)))
