from copy import deepcopy
from pathlib import Path


def parse_input(path: str) -> list[list[str]]:
    p = Path(__file__).resolve().parent / path
    return [list(line) for line in p.read_text().splitlines()]


def inflate_grid(grid: list[list[str]]):
    _grid = deepcopy(grid)
    grid_h = len(grid)
    grid_l = len(grid[0])
    for row_idx in range(grid_h - 1, -1, -1):
        row = grid[row_idx]
        if all(elt == "." for elt in row):
            _grid.insert(row_idx, ["."] * grid_h)

    for col_idx in range(grid_l - 1, -1, -1):
        if all(row[col_idx] == "." for row in grid):
            for row in _grid:
                row.insert(col_idx, ".")

    return _grid


def get_empty_spaces(grid: list[list[str]]) -> tuple[list[int], list[int]]:
    empty_rows, empty_cols = [], []

    empty_rows = [int(all(elt == "." for elt in row)) for row in grid]
    empty_cols = [
        int(all(row[col_idx] == "." for row in grid)) for col_idx in range(len(grid[0]))
    ]
    return empty_rows, empty_cols


def get_galaxy_positions(grid: list[list[str]]) -> set[tuple[int]]:
    return {
        (row_idx, col_idx)
        for row_idx, line in enumerate(grid)
        for col_idx, elt in enumerate(line)
        if elt == "#"
    }


def get_distances(
    galaxies: list[tuple[int, int]],
    empty_spaces: tuple[list[int], list[int]] = None,
    empty_size=1,
) -> list[int]:
    empty_h, empty_l = empty_spaces or ([], [])
    res = []
    for idx1, gal1 in enumerate(galaxies):
        for gal2 in galaxies[idx1 + 1 :]:
            min_h = min(gal1[0], gal2[0])
            max_h = max(gal1[0], gal2[0])
            min_l = min(gal1[1], gal2[1])
            max_l = max(gal1[1], gal2[1])

            empty_crossed_h = sum(elt for elt in empty_h[min_h : max_h + 1])
            empty_crossed_l = sum(elt for elt in empty_l[min_l : max_l + 1])
            res.append(
                abs(gal1[0] - gal2[0])
                + abs(gal1[1] - gal2[1])
                + (empty_crossed_h + empty_crossed_l) * empty_size
            )
    return res


def resolve1():
    grid = parse_input("input_example.txt")
    empty_spaces = get_empty_spaces(grid)

    # print("\n".join("".join(row) for row in grid))

    galaxies = list(get_galaxy_positions(grid))
    return sum(dist for dist in get_distances(galaxies, empty_spaces, 1))


def resolve2():
    grid = parse_input("input.txt")
    empty_spaces = get_empty_spaces(grid)

    # print("\n".join("".join(row) for row in grid))

    galaxies = list(get_galaxy_positions(grid))
    return sum(dist for dist in get_distances(galaxies, empty_spaces, 1000000 - 1))


if __name__ == "__main__":
    print(resolve1())
    print(resolve2())
