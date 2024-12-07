from pathlib import Path


def parse_input(path: str):
    p = Path(__file__).resolve().parent / path

    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return content.split("\n")


Position = tuple[int, int]
Direction = tuple[int, int]


DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class Grid:
    def __init__(
        self, grid: list[list[str]], extra_wall_pos: Position | None = None
    ) -> None:
        self.grid = grid
        self.extra_wall_pos = extra_wall_pos
        self._len = None

    def __getitem__(self, pos: Position) -> str:
        if pos == self.extra_wall_pos:
            return "#"
        return self.grid[pos[0]][pos[1]]

    def __len__(self):
        if self._len is None:
            self._len = len(self.grid)
        return self._len

    def get_first_pos(self) -> Position:
        for x in range(len(self)):
            for y in range(len(self)):
                if self[(x, y)] == "^":
                    return (x, y)
        raise Exception("No start position found")


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
        if grid[(x, y)] == "#":
            return visited, False
        visited.append((x, y))


def resolve1():
    grid = Grid(parse_input("input.txt"))
    pos = grid.get_first_pos()
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


def has_loop(grid: Grid) -> bool:

    pos = grid.get_first_pos()
    direction_index = 0
    state_hashes = set()

    visited: set[Position] = set()
    while True:
        _visited, is_end = move(pos, grid, DIRECTIONS[direction_index])
        visited.update(_visited)
        if is_end:
            return False

        if _visited:
            pos = _visited[-1]

        direction_index = (direction_index + 1) % 4

        if (state_hash := hash((pos, direction_index, tuple(visited)))) in state_hashes:
            return True
        else:
            state_hashes.add(state_hash)


def resolve2():

    _grid = parse_input("input.txt")
    n = len(_grid)
    print(n)
    res = 0
    for x in range(n):
        for y in range(n):
            print(x, y)
            if _grid[x][y] == ".":
                grid = Grid(_grid, (x, y))
                res += 1 if has_loop(grid) else 0
    return res


if __name__ == "__main__":
    print(resolve1())
    print(resolve2())
