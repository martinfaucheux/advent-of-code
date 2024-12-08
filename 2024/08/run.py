from pathlib import Path
from collections import defaultdict

Grid = list[str]
Position = tuple[int, int]


def parse_input(path: str):
    p = Path(__file__).resolve().parent / path

    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return content.split("\n")


def get_groups(grid: Grid) -> dict[str, set[Position]]:
    res = defaultdict(set)
    n = len(grid)
    for x in range(n):
        for y in range(n):
            if grid[x][y] != ".":
                res[grid[x][y]].add((x, y))
    return res


def get_antinodes(
    grid: Grid, positions: set[Position], first_only=True
) -> set[Position]:
    nodes: set[Position] = set()
    for pos1 in positions:
        x1, y1 = pos1
        for pos2 in positions:
            if pos1 == pos2:
                continue
            x2, y2 = pos2

            dx = x2 - x1
            dy = y2 - y1

            count = 1 if first_only else 0
            while True:

                x = x1 - count * dx
                y = y1 - count * dy

                if not is_valid_pos(grid, (x, y)):
                    break

                nodes.add((x, y))
                count += 1

                if first_only:
                    break

    return nodes


def is_valid_pos(grid: Grid, pos: Position):
    x, y = pos
    return 0 <= x < len(grid) and 0 <= y < len(grid[x])


def resolve1():
    grid = parse_input("input.txt")
    assert len(grid) == len(grid[0])
    nodes: set[Position] = set()

    position_groups = get_groups(grid)
    for group in position_groups.values():
        nodes |= get_antinodes(grid, group)

    return len(nodes)


def resolve2():
    grid = parse_input("input.txt")
    assert len(grid) == len(grid[0])
    nodes: set[Position] = set()

    position_groups = get_groups(grid)
    for group in position_groups.values():
        nodes |= get_antinodes(grid, group, first_only=False)

    return len(nodes)


if __name__ == "__main__":
    print(resolve1())
    print(resolve2())
