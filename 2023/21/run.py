import json
from collections.abc import Generator
from copy import deepcopy
from dataclasses import dataclass
from itertools import chain
from pathlib import Path

JSON_MAP_PATH = "touch_map.json"

Grid = list[list[str]]
Pos = tuple[int, int]


def parse_input(path: str):
    p = Path(__file__).resolve().parent / path
    return [list(line) for line in p.read_text().splitlines()]


def get_neighbors(grid: Grid, pos: Pos):
    x, y = pos
    res = set()
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        _x, _y = x + dx, y + dy
        if is_valid_pos(grid, (_x, _y)) and grid[_x][_y] != "#":
            res.add((_x, _y))
    return res


def is_valid_pos(grid: Grid, pos: Pos):
    x, y = pos
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])


def incr(grid: Grid, pos_list: set[Pos]):
    res = set()
    for pos in pos_list:
        res |= get_neighbors(grid, pos)
    return res


def incr_n(grid: Grid, pos: Pos, n: int):
    pos_list = {pos}
    for _ in range(n):
        pos_list = incr(grid, pos_list)
    return pos_list


def get_start_pos(grid):
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] == "S":
                return (x, y)


def resolve1():
    grid = parse_input("input.txt")
    pos_list = {get_start_pos(grid)}
    pos_list = incr_n(grid, get_start_pos(grid), 64)
    return len(pos_list)


def get_border_pos(grid: Grid) -> Generator[Pos]:
    return chain(
        ((x, 0) for x in range(len(grid))),
        ((x, len(grid[0]) - 1) for x in range(len(grid))),
        ((0, y) for y in range(len(grid[0]))),
        ((len(grid) - 1, y) for y in range(len(grid[0]))),
    )


def get_touch_counts(grid: Grid, init_pos: Pos) -> dict[Pos, int]:
    step = 0
    touches: dict[Pos, int] = {(x, y): -1 for x, y in get_border_pos(grid)}

    positions: set[Pos] = {init_pos}
    while any(distance == -1 for distance in touches.values()):
        step += 1
        positions = incr(grid, positions)
        for pos in positions:
            if pos in touches and touches[pos] == -1:
                touches[pos] = step
    return touches


def tuple_to_str(_map: dict[Pos, dict[Pos, int]]):
    def conv(t):
        return "_".join(str(e) for e in t)

    return {
        conv(base_pos): {conv(k): v for k, v in touches.items()}
        for base_pos, touches in _map.items()
    }


def build_touch_map(grid: Grid):
    touch_map: dict[Pos, dict[Pos, int]] = {}
    for border_pos in get_border_pos(grid):
        touch_map[border_pos] = get_touch_counts(grid, border_pos)

    p = Path(__file__).resolve().parent / JSON_MAP_PATH
    p.write_text(json.dumps(tuple_to_str(touch_map)))
    print("Map saved!")


def build_sector_map(grid: Grid):
    pass


def color(grid: Grid, positions: set[Pos]) -> str:
    _color = deepcopy(grid)
    for x, y in positions:
        _color[x][y] = "O"
    return _color


def to_str(grid: Grid):
    return "\n".join("".join(line) for line in grid)


def save(grid: Grid, path: str = "draw.txt"):
    p = Path(__file__).resolve().parent / path
    p.write_text(to_str(grid))


class Sector:
    pos: Pos
    intrusions: dict[Pos, int]


def get_mega_pos_count(grid: Grid) -> int:
    get_start_pos = get_start_pos(grid)

    s0 = Sector((0, 0), 0)
    sectors: dict[Pos, Sector] = {(0, 0)}


if __name__ == "__main__":
    grid = parse_input("input.txt")
    start_pos = get_start_pos(grid)

    print(len(grid), len(grid[0]))
    print(start_pos)
    # touches = get_touch_counts(grid, start_pos)

    # first_touch = min(touches, key=lambda x: touches[x])

    # positions = incr_n(grid, start_pos, touches[first_touch])
    # res = color(grid, positions)
    # save(res)
    # print("drawing saved!")
