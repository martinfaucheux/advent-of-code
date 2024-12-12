from pathlib import Path

Pos = tuple[int, int]

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def parse_input(path: str) -> list[str]:
    p = Path(__file__).resolve().parent / path

    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return content.split("\n")


def get_group(grid: list[str], pos: Pos) -> tuple[set[Pos], int]:
    x, y = pos
    value = grid[x][y]
    seen: set[Pos] = set()
    to_visit: set[Pos] = {pos}
    edge_count = 0
    while to_visit:
        current = to_visit.pop()
        seen.add(current)
        for dx, dy in DIRECTIONS:
            tx, ty = (current[0] + dx, current[1] + dy)
            if (tx, ty) not in seen:
                if is_valid_pos(grid, (tx, ty)) and grid[tx][ty] == value:
                    seen.add((tx, ty))
                    to_visit.add((tx, ty))
                else:
                    edge_count += 1
    return seen, edge_count


def is_valid_pos(grid: list[str], pos: Pos) -> bool:
    x, y = pos
    return (x >= 0) and (x < len(grid)) and (y >= 0) and (y < len(grid[x]))


def resolve1():
    grid = parse_input("input.txt")
    seen: set[Pos] = set()
    res = 0
    for x in range(len(grid)):
        for y in range(len(grid)):
            if (x, y) not in seen:
                group, edge_count = get_group(grid, (x, y))
                res += len(group) * edge_count
                seen |= group
    return res


def resolve2():
    grid = parse_input("input_example.txt")

    return 0


if __name__ == "__main__":
    print(resolve1())
    print(resolve2())
