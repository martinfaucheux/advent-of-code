from pathlib import Path
from enum import Enum

Pos = tuple[int, int]

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def parse_input(path: str) -> list[str]:
    p = Path(__file__).resolve().parent / path

    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return content.split("\n")


def get_group(grid: list[str], pos: Pos) -> tuple[set[Pos], int]:
    x, y = pos
    value = grid[x][y]
    seen: set[Pos] = set()
    to_visit: set[Pos] = {pos}
    edges: set[Edge] = set()
    while to_visit:
        current = to_visit.pop()
        seen.add(current)
        for dx, dy in DIRECTIONS:
            tx, ty = (current[0] + dx, current[1] + dy)
            if (tx, ty) not in seen:
                if is_valid_pos(grid, (tx, ty)) and grid[tx][ty] == value:
                    seen.add((tx, ty))
                    to_visit.add((tx, ty))
                else:
                    edge = get_edge_between(current, (dx, dy))
                    adjacent_edges = {e for e in edges if e.get_joint(edge) is not None}
                    new_edge = Edge.merge(edge, *adjacent_edges)
                    edges -= adjacent_edges
                    edges.add(new_edge)

    return seen, edges


def get_edge_between(pos: Pos, dir: Pos) -> "Edge":
    x, y = pos
    if dir == (-1, 0):
        p1 = (x, y)
        p2 = (x, y + 1)
    elif dir == (0, 1):
        p1 = (x, y + 1)
        p2 = (x + 1, y + 1)
    elif dir == (1, 0):
        p1 = (x + 1, y)
        p2 = (x + 1, y + 1)
    elif dir == (0, -1):
        p1 = (x, y)
        p2 = (x + 1, y)
    else:
        raise ValueError(f"Invlid direction: {dir}")
    return Edge(p1, p2)


class EdgeType(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class Edge:
    p1: Pos
    p2: Pos

    def __init__(self, p1: Pos, p2: Pos):

        if not (p1[0] <= p2[0] and p1[1] <= p2[1]):
            p1, p2 = p2, p1

        if not (p1[0] == p2[0] or p1[1] == p2[1]):
            raise ValueError("edge must be either vertical or hozizontal")

        if p1 == p2:
            raise ValueError("edge cannot be empty")

        self.p1 = p1
        self.p2 = p2

    def __gt__(self, other: "Edge") -> bool:
        if self.type != other.type:
            raise ValueError("edges must be of the same type")

        if self.type == EdgeType.HORIZONTAL:
            # horizontal => x is constant
            return self.p1[1] > other.p1[1]
        else:
            # vertical => y is constant
            return self.p1[0] > other.p1[0]

    def __hash__(self):
        return hash((self.p1, self.p2))

    def __repr__(self) -> str:
        return f"E[{self.p1}:{self.p2}]"

    def get_joint(self, other: "Edge") -> Pos | None:
        if self.type == other.type:
            if self.p1 == other.p2:
                return self.p1
            elif self.p2 == other.p1:
                return self.p2
        return None

    @property
    def type(self) -> EdgeType:
        return EdgeType.HORIZONTAL if self.p1[0] == self.p2[0] else EdgeType.VERTICAL

    @property
    def size(self) -> int:
        return abs(self.p1[0] - self.p2[0]) + abs(self.p1[1] - self.p2[1])

    @classmethod
    def merge(cls, edge: "Edge", *edges) -> "Edge":
        if len(edges) == 0:
            return edge
        else:
            return cls.merge(cls._merge(edge, edges[0]), *edges[1:])

    @staticmethod
    def _merge(e1: "Edge", e2: "Edge") -> "Edge":
        if e1.get_joint(e2) is None:
            raise ValueError(f"cannot merge non adjacent edges: {e1} {e2}")
        e1, e2 = (e1, e2) if e2 > e1 else (e2, e1)
        return Edge(e1.p1, e2.p2)


def is_valid_pos(grid: list[str], pos: Pos) -> bool:
    x, y = pos
    return (x >= 0) and (x < len(grid)) and (y >= 0) and (y < len(grid[x]))


def resolve1():
    grid = parse_input("input.txt")
    seen: set[Pos] = set()
    res = 0
    for x in range(len(grid)):
        for y in range(len(grid)):
            if (x, y) not in seen:
                group, edges = get_group(grid, (x, y))
                res += len(group) * sum(edge.size for edge in edges)
                seen |= group
    return res


def resolve2():
    grid = parse_input("test_input.txt")
    seen: set[Pos] = set()
    res = 0
    for x in range(len(grid)):
        for y in range(len(grid)):
            if (x, y) not in seen:
                group, edges = get_group(grid, (x, y))
                res += len(group) * len(edges)
                seen |= group
    return res


if __name__ == "__main__":
    print(resolve1())
    print(resolve2())

    # 865906
    # too low
