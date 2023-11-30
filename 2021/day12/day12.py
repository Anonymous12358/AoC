import networkx as nx


def create_graph(inp):
    graph = nx.Graph()
    for line in inp:
        nodes = line.split("-")
        if nodes[0] not in graph:
            graph.add_node(nodes[0])
        if nodes[1] not in graph:
            graph.add_node(nodes[1])
        graph.add_edge(nodes[0], nodes[1])
    return graph


def part_a(inp):
    graph = create_graph(inp)
    stack = [("start", {"start"})]  # [(current location, {small caves visited}),...]
    routes = 0
    while stack:
        curr = stack.pop()
        if curr[0] == "end":
            routes += 1
        else:
            for neighbour in set(graph.neighbors(curr[0])) - curr[1]:
                stack.append((neighbour, curr[1] | ({neighbour} if neighbour.islower() else set())))
    return routes


def part_b(inp):
    graph = create_graph(inp)
    stack = [("start", {"start"}, False)]  # [(current location, {small caves visited}, visited a small cave twice),...]
    routes = 0
    while stack:
        curr = stack.pop()
        if curr[0] == "end":
            routes += 1
            continue

        if curr[2]:
            for neighbour in set(graph.neighbors(curr[0])) - curr[1]:
                stack.append((neighbour, curr[1] | ({neighbour} if neighbour.islower() else set()), True))
        else:
            for neighbour in set(graph.neighbors(curr[0])) - {"start"}:
                stack.append((neighbour, curr[1] | ({neighbour} if neighbour.islower() else set()), neighbour in curr[1]))
    return routes
