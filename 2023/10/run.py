from collections import deque
from functools import reduce
from pathlib import Path

# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

_CHAR_COORD = {
    "|": [(-1, 0), (1, 0)],
    "-": [(0, -1), (0, 1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(0, -1), (-1, 0)],
    "7": [(0, -1), (1, 0)],
    "F": [(1, 0), (0, 1)],
}

CHAR_MAP = {k: {v1: v2, v2: v1} for k, (v1, v2) in _CHAR_COORD.items()}


def parse_input(path: str):
    p = Path(__file__).resolve().parent / path
    content = p.read_text().splitlines()
    return content


def save(draw, path="draw.txt"):
    p = Path(__file__).resolve().parent / path
    p.write_text(draw)


def get_start_pos(table):
    for row, line in enumerate(table):
        try:
            col = line.index("S")
            return row, col
        except ValueError:
            continue
    raise ValueError("No start position found")


def is_valid_pos(table, pos):
    row, col = pos
    return 0 <= row < len(table) and 0 <= col < len(table[row])


def inverse_dir(dir):
    return (dir[0] * -1, dir[1] * -1)


def get_circle(grid):
    pos = get_start_pos(grid)
    step = 0
    draw_grid = ["." * len(grid[0]) for _ in range(len(grid))]

    visited = [{pos}] * 4
    position_list = [(pos, dir) for dir in [(0, 1), (1, 0), (0, -1), (-1, 0)]]
    dead_ends = [False] * 4
    while True:
        step += 1
        if all(dead_ends):
            raise Exception("Only dead end found")

        for idx, ((pos, dir), dead_end) in enumerate(zip(position_list, dead_ends)):
            if dead_end:
                continue

            x, y = pos
            draw_grid[x] = draw_grid[x][:y] + str(step) + draw_grid[x][y + 1 :]

            x, y = (x + dir[0], y + dir[1])
            next_pos = (x, y)

            if any(next_pos in v for v in visited):
                # return step
                return reduce(
                    lambda s1, s2: s1 | s2,
                    (s for idx, s in enumerate(visited) if not dead_ends[idx]),
                    set(),
                )

            if (not is_valid_pos(grid, next_pos)) or (next_val := grid[x][y]) == ".":
                dead_ends[idx] = True
                continue

            if next_val == "S":
                raise Exception("This case should not happen")

            inv_dir = inverse_dir(dir)
            try:
                next_dir = CHAR_MAP[next_val][inv_dir]
            except KeyError:
                dead_ends[idx] = True
                continue

            visited[idx].add(next_pos)
            position_list[idx] = (next_pos, next_dir)

        if step > 10_000_000:
            raise Exception("Max iteration")


def resolve1():
    grid = parse_input("input.txt")
    circle = get_circle(grid)
    return len(circle) // 2


def draw_circle(grid, circle):
    draw = [[" "] * len(grid[0]) for _ in range(len(grid))]
    for x, y in circle:
        draw[x][y] = "."

    draw[70][70] = "O"
    return "\n".join("".join(line) for line in draw)


def get_center_size(circle, pos, acc):
    for dir in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        next_pos = (pos[0] + dir[0], pos[1] + dir[1])

        if next_pos in acc or next_pos in circle:
            continue

        else:
            acc.add(next_pos)
            acc = get_center_size(circle, next_pos, acc)

    return acc


def fill_holes(grid, start_pos=None, filler="O"):
    if start_pos is None:
        start_pos = (len(grid) // 2, len(grid[0]) // 2)

    filled_pos = propagate(grid, start_pos)

    return [
        "".join(
            filler if (row, col) in filled_pos else elt for col, elt in enumerate(line)
        )
        for row, line in enumerate(grid)
    ]


def propagate(grid, start_pos):
    x, y = start_pos
    assert grid[x][y] == ".", "start point must be empty"

    visited = set(start_pos)
    queue = deque([start_pos])

    while queue:
        pos = queue.pop()
        visited.add(pos)

        for dir in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_pos = (pos[0] + dir[0], pos[1] + dir[1])
            x, y = next_pos
            if (
                (not is_valid_pos(grid, next_pos))
                or (next_pos in visited)
                or grid[x][y] != "."
            ):
                continue
            queue.append(next_pos)
    return visited


def inflate_grid(grid):
    _grid = []
    for row, line in enumerate(grid):
        _line1 = ""
        _line2 = ""
        for col, elt in enumerate(line):
            _line1 += elt
            if elt in ["S", "F", "L", "-"]:
                _line1 += "-"
            else:
                _line1 += "."

            if elt in ["S", "F", "7", "|"]:
                _line2 += "|."
            else:
                _line2 += ".."
        _grid.extend([_line1, _line2])
    return _grid


def reduce_grid(grid):
    return [
        "".join(elt for col, elt in enumerate(line) if col % 2 == 0)
        for row, line in enumerate(grid)
        if row % 2 == 0
    ]


def get_drawing(grid, show_sym=True):
    def tr(elt):
        if elt == ".":
            return " "
        if (not show_sym) and elt != "O":
            return " "
        return elt

    return "\n".join("".join(tr(elt) for elt in line) for line in grid)


if __name__ == "__main__":
    print(resolve1())

    grid = parse_input("input.txt")
    start_pos = (70, 70)
    circle = get_circle(grid)

    grid = [
        "".join(elt if (row, col) in circle else "." for col, elt in enumerate(line))
        for row, line in enumerate(grid)
    ]
    print(get_drawing(fill_holes(grid, start_pos)))

    grid = inflate_grid(grid)
    grid = fill_holes(grid, (start_pos[0] * 2, start_pos[1] * 2))
    grid = reduce_grid(grid)

    save(get_drawing(grid, False))
    print(sum(1 for row in grid for elt in row if elt == "O"))
