from collections import defaultdict
from dataclasses import dataclass

import networkx as nx

THRESHOLDS = {15: 1500, 12: 2000, 9: 2500, 6: 3000}


@dataclass(frozen=True)
class State:
    positions: tuple[str, str]
    open: frozenset[str]


def step_one_animal(state: State, who: int, multiplier: int, graph: nx.Graph, rates: dict[str, int]):
    if state.positions[who] not in state.open and rates[state.positions[who]] > 0:
        yield State(state.positions, state.open | {state.positions[who]}), rates[state.positions[who]] * multiplier

    for adjacent in graph[state.positions[who]]:
        yield State(state.positions[:who] + (adjacent,) + state.positions[who+1:], state.open), 0


def step(state: State, multiplier: int, graph: nx.Graph, rates: dict[str, int], has_elephant: bool):
    human_states = step_one_animal(state, 0, multiplier, graph, rates)
    if not has_elephant:
        yield from human_states
    else:
        for human_state, human_increase in human_states:
            for state, elephant_increase in step_one_animal(human_state, 1, multiplier, graph, rates):
                yield state, human_increase + elephant_increase


def search(start: State, graph: nx.Graph, rates: dict[str, int], has_elephant: bool):
    states = {start: 0}
    threshold = 0
    for multiplier in range(29 - 4 * has_elephant, 0, -1):
        if len(states) > 200_000:
            threshold = max(states.values()) * 0.8
        new_states = defaultdict(int)
        for state, score in states.items():
            for new_state, score_increase in step(state, multiplier, graph, rates, has_elephant):
                new_states[new_state] = max(new_states[new_state], score + score_increase)
                if new_states[new_state] < threshold:
                    del new_states[new_state]

        states = new_states
    return max(states.values())


def part_a(inp):
    r"""
    /Valve (\w{2}) has flow rate=(\d+); tunnels? leads? to valves? (.+)/
    str int str
    """
    rates = {}
    graph = nx.Graph()
    for name, rate, adjacents in inp:
        rates[name] = rate
        for adjacent in adjacents.split(", "):
            graph.add_edge(name, adjacent)

    start = State(("AA", "AA"), frozenset())
    return search(start, graph, rates, False)


def part_b(inp):
    r"""
    /Valve (\w{2}) has flow rate=(\d+); tunnels? leads? to valves? (.+)/
    str int str
    """
    rates = {}
    graph = nx.Graph()
    for name, rate, adjacents in inp:
        rates[name] = rate
        for adjacent in adjacents.split(", "):
            graph.add_edge(name, adjacent)

    start = State(("AA", "AA"), frozenset())
    return search(start, graph, rates, True)
