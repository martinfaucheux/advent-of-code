from math import inf
from pathlib import Path

import numpy as np

Pos = tuple[int, int]


def parse_input(path: str) -> list[tuple[str, int, str]]:
    p = Path(__file__).resolve().parent / path

    return [
        (_dir, int(l), _str[2:-1])
        for _dir, l, _str in (line.split() for line in p.read_text().splitlines())
    ]


def color_to_instr(color) -> tuple[str, int]:
    return "RDLU"[int(color[-1])], int(color[:-1], 16)


def add_tuple(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])


def instr_to_tuple(_dir: str, l: int):
    match _dir:
        case "U":
            return (-l, 0)
        case "D":
            return (l, 0)
        case "L":
            return (0, -l)
        case "R":
            return (0, l)
        case _:
            raise ValueError(f"Invalid value {_dir}")


def get_offset(d1, d2):
    match d := "".join(sorted(d1 + d2)):
        case "DR":
            x, y = (-1, 1)
        case "DL":
            x, y = (1, 1)
        case "LU":
            x, y = (1, -1)
        case "RU":
            x, y = (-1, -1)
        case _:
            raise ValueError(f"Invalid direction: {d}")
    return 0.5 * x, 0.5 * y


def get_coords(instr_list):
    # TODO: here we miss 1 tile
    base_pos = (0, 0)
    pos_list = []
    for idx, (_dir, l) in enumerate(instr_list):
        base_pos = add_tuple(base_pos, instr_to_tuple(_dir, l))
        next_dir = instr_list[(idx + 1) % len(instr_list)][0]
        offset = get_offset(_dir, next_dir)
        pos_list.append(add_tuple(base_pos, offset))

    # assert add_tuple(pos, instr_to_tuple(*instr_list[-1][:2])) == (0, 0)
    return pos_list


def shoelace(coords: list[Pos]) -> int:
    return (
        sum(
            (coords[idx][1] + coords[(idx + 1) % len(coords)][1] + 1)
            * (coords[(idx + 1) % len(coords)][0] - coords[idx][0])
            for idx in range(len(coords))
        )
        / 2
    )


def np_shoelace(x_y):
    x_y = np.array(x_y)
    x_y = x_y.reshape(-1, 2)

    x = x_y[:, 0]
    y = x_y[:, 1]

    S1 = np.sum(x * np.roll(y, -1))
    S2 = np.sum(y * np.roll(x, -1))

    area = 0.5 * np.absolute(S1 - S2)

    return area


def resolve1():
    lines = parse_input("input.txt")
    coords = get_coords([(a, b) for a, b, _ in lines])
    return shoelace(coords)


def resolve2():
    lines = parse_input("input.txt")
    coords = get_coords([color_to_instr(color) for _, _, color in lines])
    return np_shoelace(coords)


"""
###.
####
####
.###
"""

if __name__ == "__main__":
    print(resolve1())
    print(resolve2())
