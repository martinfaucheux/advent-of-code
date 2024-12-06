from pathlib import Path


def parse_input(path: str):
    p = Path(__file__).resolve().parent / path

    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return content.split("\n")


Position = tuple[int, int]
Direction = tuple[int, int]
Grid = list[list[str]]


DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def move(pos: Position, grid: Grid, dir: Direction) -> tuple[list[Position], bool]:
    n = len(grid)
    visited = []
    x, y = pos
    dx, dy = dir
    while True:
        x += dx
        y += dy
        if (x < 0) or (x >= n) or (y < 0) or (y >= n):
            return visited, True
        if grid[x][y] == "#":
            return visited, False
        visited.append((x, y))


def get_first_pos(grid: Grid) -> Position:
    n = len(grid)
    for x in range(n):
        for y in range(n):
            if grid[x][y] == "^":
                return (x, y)
    raise Exception("No start position found")


def resolve1():
    grid = parse_input("input.txt")
    assert len(grid) == len(grid[0])
    pos = get_first_pos(grid)
    direction_index = 0

    visited: set[Position] = set()
    while True:
        _visited, is_end = move(pos, grid, DIRECTIONS[direction_index])
        visited.update(_visited)
        if is_end:
            break

        if _visited:
            pos = _visited[-1]

        direction_index = (direction_index + 1) % 4

    return len(visited)


def resolve2():
    grid = parse_input("input_example.txt")
    n = len(grid)

    return 0


if __name__ == "__main__":
    print(resolve1())
    print(resolve2())
