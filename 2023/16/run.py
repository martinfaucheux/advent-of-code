from collections import defaultdict
from pathlib import Path

Grid = list[list[str]]
Pos = tuple[int, int]
Dir = int
VisitList = defaultdict[Pos : set[Dir]]


def add_dir(pos: Pos, dir: Dir) -> Pos:
    match dir:
        case 0:
            dir_vect = (-1, 0)  # up
        case 1:
            dir_vect = (0, -1)  # left
        case 2:
            dir_vect = (1, 0)  # down
        case 3:
            dir_vect = (0, 1)  # right
        case _:
            raise ValueError(f"Invalid direction: {dir}")
    return tuple(v1 + v2 for v1, v2 in zip(pos, dir_vect))


def parse_input(path: str):
    p = Path(__file__).resolve().parent / path
    return [list(line) for line in p.read_text().split("\n")]


def is_valid_position(grid: Grid, pos: Pos):
    x, y = pos
    return 0 <= x < len(grid) and 0 <= y < len(grid[x])


def follow(
    grid: Grid, pos: Pos, dir: Dir, visited: VisitList | None = None
) -> VisitList:
    if visited is None:
        visited = defaultdict(set)
    x, y = pos
    val = grid[x][y]
    print(sum(len(v) for v in visited.values()))

    visited[pos].add(dir)
    tuples = []
    match val:
        case ".":
            tuples.append((add_dir(pos, dir), dir))
        case "-":
            if dir % 2 == 1:
                # go through
                tuples.append((add_dir(pos, dir), dir))
            else:
                # split up and down
                for new_dir in [1, 3]:
                    tuples.append((add_dir(pos, new_dir), new_dir))
        case "|":
            if dir % 2 == 0:
                # go through
                tuples.append((add_dir(pos, dir), dir))
            else:
                # split up and down
                for new_dir in [0, 2]:
                    tuples.append((add_dir(pos, new_dir), new_dir))
        case "/":
            conv = {0: 1, 1: 0, 2: 3, 3: 2}
            new_dir = conv[(dir + 2) % 4]
            tuples.append((add_dir(pos, new_dir), new_dir))
        case "\\":
            conv = {0: 3, 1: 2, 2: 1, 3: 0}
            new_dir = conv[(dir + 2) % 4]
            tuples.append((add_dir(pos, new_dir), new_dir))
        case _:
            raise ValueError(f"Invalid char: {val}")

    for new_pos, new_dir in tuples:
        if is_valid_position(grid, new_pos) and new_dir not in visited[new_pos]:
            follow(grid, new_pos, new_dir, visited)

    return visited


def color(grid, visited):
    _grid = [["." for _ in range(len(grid[0]))] for _ in range(len(grid))]
    for x, y in visited:
        _grid[x][y] = "#"
    return _grid


def gprint(grid):
    print("\n".join("".join(row) for row in grid))


def resolve1():
    grid = parse_input("input_example3.txt")
    visited = follow(grid, (0, 0), 3)

    return visited


if __name__ == "__main__":
    grid = parse_input("input.txt")
    visited = follow(grid, (0, 0), 3)

    gprint(color(grid, visited))
