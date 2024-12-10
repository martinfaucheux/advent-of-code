from pathlib import Path
from collections import defaultdict
from functools import lru_cache

Pos = tuple[int, int]

Grid = tuple[tuple[int, ...], ...]

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def parse_input(path: str):
    p = Path(__file__).resolve().parent / path

    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return tuple(tuple(int(elt) for elt in line) for line in content.split("\n"))


def is_valid_pos(grid: Grid, pos: Pos):
    return 0 <= pos[0] < len(grid) and 0 <= pos[1] < len(grid[0])


@lru_cache
def get_reachable_nines(grid: Grid, pos: Pos) -> tuple[Pos, ...]:
    x, y = pos
    value = grid[x][y]
    if value == 9:
        return tuple({pos})
    res = tuple()
    for dx, dy in DIRECTIONS:
        tx, ty = (x + dx, y + dy)
        if is_valid_pos(grid, (tx, ty)) and grid[tx][ty] == (value + 1):
            res = merge_tuples(res, get_reachable_nines(grid, (tx, ty)))
    return res


@lru_cache
def get_distinct_trail_count(grid: Grid, pos: Pos) -> int:
    x, y = pos
    value = grid[x][y]
    if value == 9:
        return 1
    res = 0
    for dx, dy in DIRECTIONS:
        tx, ty = (x + dx, y + dy)
        if is_valid_pos(grid, (tx, ty)) and grid[tx][ty] == (value + 1):
            res += get_distinct_trail_count(grid, (tx, ty))
    return res


def merge_tuples(t1: tuple[Pos, ...], t2: tuple[Pos, ...]) -> tuple[Pos, ...]:
    return set(set(t1) | set(t2))


def get_map_score(grid: Grid):
    n = len(grid)
    return sum(
        len(get_reachable_nines(grid, (x, y)))
        for x in range(n)
        for y in range(n)
        if grid[x][y] == 0
    )


def get_map_rating(grid: Grid):
    n = len(grid)
    return sum(
        get_distinct_trail_count(grid, (x, y))
        for x in range(n)
        for y in range(n)
        if grid[x][y] == 0
    )


def test():
    for test_id, exp_res in enumerate(
        [
            0,
            1,
        ]
    ):
        grid = parse_input(f"test_cases/test{test_id +1 }.txt")
        score = get_map_score(grid)
        assert (
            score == exp_res
        ), f"Invalid test case {test_id + 1}: expected {exp_res}, got {score}"


def resolve1():
    test()
    grid = parse_input("input.txt")

    return get_map_score(grid)


def resolve2():

    grid = parse_input("input.txt")
    return get_map_rating(grid)


if __name__ == "__main__":
    print(resolve1())
    print(resolve2())
