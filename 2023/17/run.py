from collections import defaultdict
from dataclasses import dataclass
from math import inf
from pathlib import Path
from queue import PriorityQueue


def parse_input(path: str):
    p = Path(__file__).resolve().parent / path
    return [[int(elt) for elt in line] for line in p.read_text().splitlines()]


class Plane:
    HORIZONTAL = 0
    VERTICAL = 1


Grid = list[list[int]]
Pos = tuple[int, int]
Coord = tuple[Pos, Plane]


@dataclass
class Node:
    pos: tuple[int, int]
    plane: Plane

    @property
    def label(self) -> str:
        return f"{self.pos[0]}_{self.pos[1]}_{self.plane}"

    def __hash__(self):
        return hash((self.pos, self.plane))

    def __lt__(self, other: "Node") -> bool:
        return (self.pos, self.plane) < (other.pos, other.plane)


@dataclass
class Edge:
    origin: Node
    dest: Node
    weight: int

    def __hash__(self):
        return hash((self.origin, self.dest))


@dataclass
class Graph:
    nodes: dict[Coord, Node]
    edges: dict[Node, set[Edge]]

    def __init__(self):
        self.nodes = {}
        self.edges = defaultdict(set)

    def add_node(self, pos: Pos, plane: Plane) -> Node:
        node = Node(pos, plane)
        self.nodes[(pos, plane)] = node
        return node

    def add_edge(self, origin: Node, dest: Node, weight: int) -> Edge:
        edge = Edge(origin, dest, weight)
        self.edges[origin].add(edge)
        return edge

    def get_node(self, pos: Pos, plane: Plane) -> Node:
        return self.nodes[(pos, plane)]


def is_valid_position(grid: Grid, pos: Pos):
    x, y = pos
    return 0 <= x < len(grid) and 0 <= y < len(grid[x])


def build_graph(grid: Grid, min_dist=1, max_dist=3):
    g = Graph()

    for plane in (0, 1):
        for row_idx in range(len(grid)):
            for col_idx in range(len(grid[0])):
                g.add_node((row_idx, col_idx), plane)

    for node in g.nodes.values():
        dir_list = (
            [
                (mult * idx, 0)
                for mult in (1, -1)
                for idx in range(min_dist, max_dist + 1)
            ]
            if node.plane == Plane.VERTICAL
            else [
                (0, mult * idx)
                for mult in (1, -1)
                for idx in range(min_dist, max_dist + 1)
            ]
        )
        for pos_diff in dir_list:
            dest_pos = (node.pos[0] + pos_diff[0], node.pos[1] + pos_diff[1])
            if is_valid_position(grid, dest_pos):
                weight = get_weight(grid, node.pos, dest_pos)

                dest_node = g.get_node(dest_pos, 1 - node.plane)
                g.add_edge(node, dest_node, weight)

    start_node1, start_node2 = g.get_node((0, 0), 0), g.get_node((0, 0), 1)
    g.add_edge(start_node1, start_node2, 0)
    g.add_edge(start_node2, start_node1, 0)

    end_pos = (len(grid) - 1, len(grid[0]) - 1)
    end_node1, end_node2 = g.get_node(end_pos, 0), g.get_node(end_pos, 1)
    g.add_edge(end_node1, end_node2, 0)
    g.add_edge(end_node2, end_node1, 0)
    return g


def get_weight(grid: Grid, origin: Pos, dest: Pos) -> int:
    diff = (dest[0] - origin[0], dest[1] - origin[1])
    weight = 0

    if r := diff[0]:
        pace = 1 if r > 0 else -1

        for x in range(origin[0] + pace, origin[0] + pace + r, pace):
            weight += grid[x][origin[1]]
        return weight
    elif r := diff[1]:
        pace = 1 if r > 0 else -1

        for y in range(origin[1] + pace, origin[1] + r + pace, pace):
            weight += grid[origin[0]][y]
        return weight

    raise ValueError(f"Invalid diff: ({diff})")


def to_mermaid(graph: Graph):
    lines = ["classDef HORIZONTAL fill:red", "classDef VERTICAL fill:green"]

    for node in graph.nodes.values():
        printable = f"{node.pos} {'v' if node.plane == Plane.VERTICAL else 'h'}"
        _class = "VERTICAL" if node.plane == Plane.VERTICAL else "HORIZONTAL"
        lines.append(f'state "{printable}" as {node.label}')
        lines.append(f"class {node.label} {_class}")

    for edge_set in graph.edges.values():
        for edge in edge_set:
            lines.append(f"{edge.origin.label} --> {edge.dest.label} : {edge.weight}")

    return "stateDiagram-v2\n" + "\n".join("\t" + line for line in lines)


def dijkstra(graph: Graph, start_node: Node, end_node: Node):
    start_node = graph.get_node((0, 0), 0)
    weight_map: dict[Node:int] = {node: inf for node in graph.nodes.values()}
    weight_map[start_node] = 0
    q = PriorityQueue()
    q.put((0, start_node))
    visited: set[Node] = set()

    while not q.empty():
        (weight, node) = q.get()
        visited.add(node)
        for edge in graph.edges[node]:
            weight = edge.weight
            neighbor_node = edge.dest
            if neighbor_node not in visited:
                old_cost = weight_map[neighbor_node]
                new_cost = weight_map[node] + weight
                if new_cost < old_cost:
                    q.put((new_cost, neighbor_node))
                    weight_map[neighbor_node] = new_cost
    return weight_map[end_node]


def resolve1():
    grid = parse_input("input.txt")
    graph = build_graph(grid)
    start_node = graph.get_node((0, 0), 0)
    end_node = graph.get_node((len(grid) - 1, len(grid[0]) - 1), 0)
    return dijkstra(graph, start_node, end_node)


def resolve2():
    grid = parse_input("input.txt")
    graph = build_graph(grid, 4, 10)
    start_node = graph.get_node((0, 0), 0)
    end_node = graph.get_node((len(grid) - 1, len(grid[0]) - 1), 0)
    return dijkstra(graph, start_node, end_node)


if __name__ == "__main__":
    print(resolve1())
    print(resolve2())
