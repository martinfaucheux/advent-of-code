from functools import cache, lru_cache
from pathlib import Path
from pprint import pprint

import numpy as np

CACHE_SIZE = 32768


def parse_input(path: str):
    p = Path(__file__).resolve().parent / path
    return tuple(p.read_text().splitlines())


def to_numpy(grid):
    repl = {"#": -1, "O": 1, ".": 0}
    return np.array([[repl[elt] for elt in row]] for row in grid)


@lru_cache(CACHE_SIZE)
def count(line: str) -> str:
    return line.count("O")


def get_weight(line: str) -> int:
    split = line.split("#")
    idx = 0
    res = 0
    for s in split:
        c = count(s)
        for _c in range(c):
            res += len(line) - idx - _c
        # add 1 for each rock
        idx += len(s) + 1
    return res


def get_instant_weight(line: str) -> int:
    res = 0
    for idx, elt in enumerate(line):
        if elt == "O":
            res += len(line) - idx
    return res


def get_grid_weight(grid):
    return sum(get_instant_weight("".join(col)) for col in zip(*grid))


@lru_cache(CACHE_SIZE)
def fall(line: str):
    split = line.split("#")
    idx = 0
    _line = ""
    for s in split:
        c = count(s)
        _line += "O" * c + "." * (len(s) - c) + "#"
        idx += len(s) + 1
    return _line[:-1]


def resolve1():
    lines = parse_input("input.txt")
    return sum(get_weight("".join(col)) for col in zip(*lines))


@lru_cache(CACHE_SIZE)
def make_cycle(grid):
    _grid = []
    for col in zip(*grid):
        _col = fall("".join(col))
        _grid.append(_col[::-1])
    return tuple(_grid)


def to_str(grid):
    grid = list(grid)
    return "\n".join("".join(row) for row in grid)


if __name__ == "__main__":
    # print(get_weight("OO.O.O..##"))
    # print(get_weight("O.#.O.O#O#"))

    # print(resolve1())

    weight = 0
    grid = parse_input("input.txt")
    for idx in range(4 * 1_000_000_000):
        grid = make_cycle(grid)
        if idx % 100_000_000 == 0:
            print(idx)

    print(to_str(grid))
    print(get_grid_weight(grid))

    #  O . # . O . O # . O
    # 10 9 8 7 6 5 4 3 2 1
