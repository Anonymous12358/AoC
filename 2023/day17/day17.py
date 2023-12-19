import numpy as np
import networkx as nx


def get_weight(y, x, d, s, inp):
    if d == 0 and s > 0:
        return sum(inp[y + step, x] for step in range(1, s + 1))
    elif d == 0 and s < 0:
        return sum(inp[y - step, x] for step in range(1, -s + 1))
    elif d == 1 and s > 0:
        return sum(inp[y, x + step] for step in range(1, s + 1))
    elif d == 1 and s < 0:
        return sum(inp[y, x - step] for step in range(1, -s + 1))


def create_edges(inp, min_distance, max_distance):
    yield from (
        ((y, x, d), (y + (1 - d) * s, x + d * s, 1 - d), {'weight': get_weight(y, x, d, s, inp)})
        for y, x in np.ndindex(inp.shape) for d in range(2)
        for abs_s in range(min_distance, max_distance + 1) for s in (abs_s, -abs_s)
        if 0 <= y + (1 - d) * s < inp.shape[0] and 0 <= x + d * s < inp.shape[1]
    )


def solve(inp, min_distance, max_distance):
    graph = nx.DiGraph()
    # Nodes represent position and facing from horizontal or vertical
    graph.add_nodes_from((y, x, d) for y, x in np.ndindex(inp.shape) for d in range(1))
    # An edge corresponds to one, two, or three steps in the same direction
    # d for direction, s for displacement (or rather signed distance)
    graph.add_edges_from(create_edges(inp, min_distance, max_distance))

    graph.add_nodes_from(("start", "end"))
    graph.add_edge("start", (0, 0, 0), weight=0)
    graph.add_edge("start", (0, 0, 1), weight=0)
    graph.add_edge((inp.shape[0] - 1, inp.shape[1] - 1, 0), "end", weight=0)
    graph.add_edge((inp.shape[0] - 1, inp.shape[1] - 1, 1), "end", weight=0)

    return nx.dijkstra_path_length(graph, source="start", target="end")


def part_a(inp):
    """array
    split
    int
    """
    return solve(inp, 1, 3)


def part_b(inp):
    """array
    split
    int
    """
    return solve(inp, 4, 10)
