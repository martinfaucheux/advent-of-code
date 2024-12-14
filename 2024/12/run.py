from pathlib import Path
from enum import Enum
from copy import deepcopy
from operator import or_
from functools import reduce
from collections import defaultdict

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

            if current == (2, 1) and (dx, dy) == (0, 1):
                pass

            if (tx, ty) not in seen:
                if is_valid_pos(grid, (tx, ty)) and grid[tx][ty] == value:
                    seen.add((tx, ty))
                    to_visit.add((tx, ty))
                else:
                    edge = get_edge_between(current, (dx, dy))

                    # 1. does it break existing edge?
                    edges = many_cuts(edge, edges)

                    # 2. can the new edge be the prolongation of existing edges?

                    joints = get_all_joints(edge, edges)

                    all_intersections = get_all_intersections(joints.keys(), edges)

                    # keep only joins where there is no existing intersection
                    adjacent_edges = {
                        e
                        for e, joints in joints.items()
                        if not (joints & all_intersections)
                    }

                    new_edge = Edge.merge(edge, *adjacent_edges)
                    edges -= adjacent_edges
                    edges.add(new_edge)
    return seen, edges


def get_all_joints(edge: "Edge", edges: "set[Edge]") -> "dict[Edge, set[Pos]]":
    res = defaultdict(set)
    for other in edges:
        if (inter := edge.get_joint(other)) is not None:
            res[other].add(inter)
    return res


def get_all_intersections(el1: "set[Edge]", el2: "set[Edge]") -> set[Pos]:
    res = set()
    for e1 in el1:
        for e2 in el2:
            if (inter := e1.get_intersection(e2)) is not None:
                res.add(inter)
    return res


def many_cuts(edge: "Edge", edges: "set[Edge]") -> "set[Edge]":
    """
    take 1 edge E1 and a list of edges. for each edge E2 of the list, split E2 by E1 if it cuts it in 2 parts
    return the mofied list with cut edges.
    """
    edges = deepcopy(edges)
    intersetions = {
        e: inter
        for e in edges
        if (inter := edge.get_intersection(e, exclude_ends=True)) is not None
    }
    edges -= {e for e in intersetions.keys()}
    return reduce(or_, (e.split(inter) for e, inter in intersetions.items()), edges)


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

    def contains(self, pos: Pos) -> bool:
        if self.type == EdgeType.HORIZONTAL:
            return self.p1[0] == pos[0] and self.p1[1] <= pos[1] <= self.p2[1]
        else:
            return self.p1[1] == pos[1] and self.p1[0] <= pos[0] <= self.p2[0]

    def get_joint(self, other: "Edge") -> Pos | None:
        if self.type == other.type:
            if self.p1 == other.p2:
                return self.p1
            elif self.p2 == other.p1:
                return self.p2
        return None

    def get_intersection(self, other: "Edge", exclude_ends=False) -> Pos | None:
        if self.type == other.type:
            return None

        h, v = (self, other) if self.type == EdgeType.HORIZONTAL else (other, self)

        if exclude_ends:
            if (v.p1[0] < h.p1[0] < v.p2[0]) and (h.p1[1] < v.p1[1] < h.p2[1]):
                return (h.p1[0], v.p1[1])
        else:
            if (v.p1[0] <= h.p1[0] <= v.p2[0]) and (h.p1[1] <= v.p1[1] <= h.p2[1]):
                return (h.p1[0], v.p1[1])
        return None

    def split(self, pos: Pos) -> "set[Edge]":
        if not self.contains(pos):
            raise ValueError(f"Cannot split {self} on {pos}")
        if pos == self.p1 or pos == self.p2:
            return {self}

        return {Edge(self.p1, pos), Edge(pos, self.p2)}

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
    grid = parse_input("input.txt")
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
