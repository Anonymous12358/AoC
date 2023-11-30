import queue
import re
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Self

pattern = re.compile(
    r'Blueprint (\d+): Each ore robot costs (\d) ore\. Each clay robot costs (\d) ore\. Each obsidian robot costs ' +
    r'(\d) ore and (\d+) clay\. Each geode robot costs (\d) ore and (\d+) obsidian\.'
)


@dataclass(frozen=True)
class State:
    resources: tuple[int, ...]
    deltas: tuple[int, ...]

    def __ge__(self, other: Self):
        return all(s >= o for s, o in zip(self.resources + self.deltas, other.resources + other.deltas))

    def __gt__(self, other: Self):
        return all(s > o for s, o in zip(self.resources + self.deltas, other.resources + other.deltas))


def step(state: State, blueprint: list[State], step_index: int = 0) -> Iterator[State]:
    could_build_geode = False
    for i, formula in reversed(list(enumerate(blueprint))):
        if i == 0 and step_index >= 20:
            continue
        elif i == 1 and step_index >= 24:
            continue
        elif step_index - i >= 28:
            continue
        if all(have >= need for have, need in zip(state.resources, formula.resources)):
            yield State(
                tuple(have - need + delta
                      for have, need, delta in zip(state.resources, formula.resources, state.deltas)),
                tuple(have + gain for have, gain in zip(state.deltas, formula.deltas))
            )
            if i == 3:
                could_build_geode = False
        if i == 2 and could_build_geode:
            return

    yield State(tuple(have + delta for have, delta in zip(state.resources, state.deltas)), state.deltas)


def geodes_bfs(start: State, blueprint: list[State], steps: int, prune_until: int = 19, prune_at=set(),
               aggro_limit: int = 30
               ) -> int:
    curr = {start}
    threshold = 0
    for i in range(steps):
        print(i, len(curr))
        if i >= aggro_limit:
            threshold = max(get_score(state, 1) for state in curr) * 0.5
        new = set()
        for state in curr:
            for new_state in step(state, blueprint, i):
                if get_score(new_state, 1) < threshold:
                    continue
                if i < prune_until or i in prune_at:
                    for other_state in set(new):
                        if new_state >= other_state:
                            new.remove(other_state)
                    if not any(other >= new_state for other in new):
                        new.add(new_state)
                else:
                    new.add(new_state)

        curr = new

    geodes = max(state.resources[-1] for state in curr)
    return geodes


SCORES = 1, 3, 5, 24, 8, 18, 30, 55


def get_score(state: State, steps_left: int) -> int:
    return sum(score * value for score, value in zip(SCORES, state.resources + state.deltas)) * steps_left


def geodes_dfs(start: State, blueprint: list[State], steps: int) -> int:
    states = queue.PriorityQueue()
    states.put((get_score(start, steps), start, steps))
    best = 0
    while states:
        _, state, steps_left = states.get()
        if steps_left == 0:
            if state.resources[-1] > best:
                print(state.resources[-1])
            best = max(best, state.resources[-1])
            continue
        for new_state in step(state, blueprint):
            states.put((get_score(start, steps), new_state, steps_left - 1))
    return best


def part_a(inp):
    print("This program takes over an hour to run on my machine. I've left printouts in so you can watch it work.")
    total = 0
    for line in inp:
        i, ore2ore, ore2clay, ore2obi, clay2obi, ore2geode, obi2geode = map(int, re.match(pattern, line).groups())
        print(i)
        blueprint = [
            State((ore2ore, 0, 0, 0), (1, 0, 0, 0)),
            State((ore2clay, 0, 0, 0), (0, 1, 0, 0)),
            State((ore2obi, clay2obi, 0, 0), (0, 0, 1, 0)),
            State((ore2geode, 0, obi2geode, 0), (0, 0, 0, 1))
        ]
        total += i * geodes_bfs(State((0, 0, 0, 0), (1, 0, 0, 0)), blueprint, 24)

    return total


def part_b(inp):
    # ans > 4158
    # should be >= 4257
    total = 1
    for line in inp[:3]:
        i, ore2ore, ore2clay, ore2obi, clay2obi, ore2geode, obi2geode = map(int, re.match(pattern, line).groups())
        print(f"{i=}")
        blueprint = [
            State((ore2ore, 0, 0, 0), (1, 0, 0, 0)),
            State((ore2clay, 0, 0, 0), (0, 1, 0, 0)),
            State((ore2obi, clay2obi, 0, 0), (0, 0, 1, 0)),
            State((ore2geode, 0, obi2geode, 0), (0, 0, 0, 1))
        ]
        total *= geodes_bfs(State((0, 0, 0, 0), (1, 0, 0, 0)), blueprint, 32, prune_until=25, aggro_limit=40)
        print(total)

    return total
