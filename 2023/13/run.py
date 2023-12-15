from copy import deepcopy
from functools import cache
from pathlib import Path


class NoSymmetryFound(Exception):
    ...


def parse_input(path: str):
    p = Path(__file__).resolve().parent / path
    return [
        tuple(
            tuple(1 if elt == "#" else 0 for elt in line)
            for line in str_grid.splitlines()
        )
        for str_grid in p.read_text().split("\n\n")
    ]


@cache
def is_reflection(array, idx):
    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # idx = 3   ^  ^
    if len(array) == 0:
        return True

    if not (0 <= idx < len(array) - 1):
        raise ValueError("Out of bound idx")

    diff = len(array) - idx - 1 - (idx + 1)
    if diff > 0:
        # > 0 : cut end
        # < 0 : cut start
        return is_reflection(array[:-diff], idx)
    if diff < 0:
        diff = -diff
        return is_reflection(array[diff:], idx - diff)

    return array[0] == array[-1] and is_reflection(array[1:-1], idx - 1)


def get_col_sym(grid):
    for col_idx in range(len(grid[0]) - 1):
        if all(is_reflection(line, col_idx) for line in grid):
            return col_idx
    return -1


def get_line_sym(grid):
    for row_idx in range(len(grid) - 1):
        if all(is_reflection(col, row_idx) for col in zip(*grid)):
            return row_idx
    return -1


def get_reflection(grid):
    if (line_sym := get_line_sym(grid)) >= 0:
        return (line_sym, -1)

    if (col_sym := get_col_sym(grid)) >= 0:
        return (-1, col_sym)

    raise NoSymmetryFound()


def get_reflection_value(x, y):
    return (x + 1) * 100 + y + 1


def get_reflection_smudge(grid):
    init_ref = get_reflection(grid)
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            try:
                ref = get_reflection(alter(grid, x, y))
                if ref != init_ref:
                    return ref
            except NoSymmetryFound:
                continue

    raise NoSymmetryFound()


def alter(grid, x, y):
    val = grid[x][y]
    grid = list(list(line) for line in grid)
    grid[x][y] = 1 - val
    return tuple(tuple(line) for line in grid)


def resolve1():
    grids = parse_input("input.txt")
    return sum(get_reflection_value(*get_reflection(grid)) for grid in grids)


def resolve2():
    grids = parse_input("input.txt")
    return sum(get_reflection_value(*get_reflection_smudge(grid)) for grid in grids)


def test_reflection():
    assert is_reflection((1, 1), 0)
    assert not is_reflection((0, 1), 0)
    assert is_reflection((0, 1, 1, 0), 1)
    assert not is_reflection((0, 1, 1, 0), 0)
    assert is_reflection((0, 1, 1, 0, 1, 1), 1)
    assert is_reflection((0, 1, 0, 1, 1, 0), 3)
    assert is_reflection(tuple("#.##..##."), 4)

    grids = parse_input("input_example.txt")
    refs = [get_reflection(g) for g in grids]

    assert refs[0] == (-1, 4), refs[0]
    assert refs[1] == (3, -1), refs[1]

    value = sum(get_reflection_value(*ref) for ref in refs)
    assert value == 405, value

    grids = parse_input("input_example.txt")
    refs = [get_reflection_smudge(grid) for grid in grids]
    assert refs == [(2, -1), (0, -1)], refs
    assert sum(get_reflection_value(*ref) for ref in refs) == 400


if __name__ == "__main__":
    test_reflection()
    print(resolve1())
    print(resolve2())
