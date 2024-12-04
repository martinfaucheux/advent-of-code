from pathlib import Path

PATTERN = "XMAS"
REV_PATTERN = PATTERN[::-1]


def parse_input(path: str):
    p = Path(__file__).resolve().parent / path

    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return [list(line) for line in content.split("\n")]


def resolve1():
    lines = parse_input("input.txt")
    assert len(lines) == len(lines[0])

    res = 0
    for str_list in [lines, zip(*lines), get_diag1(lines), get_diag2(lines)]:
        for st in str_list:
            st = "".join(st)
            res += st.count(PATTERN) + st.count(REV_PATTERN)

    return res


def get_diag1(lines):
    n = len(lines)
    return [
        [lines[i + j][j] for j in range(n) if i + j >= 0 and i + j < n]
        for i in range(-n + 1, n)
    ]


def get_diag2(lines):
    n = len(lines)
    return [
        [lines[i - j][j] for j in range(n) if i - j >= 0 and i - j < n]
        for i in range(0, 2 * n)
    ]


def is_x(lines, x, y):
    return (
        (lines[x - 1][y - 1] == "M" and lines[x + 1][y + 1] == "S")
        or (lines[x - 1][y - 1] == "S" and lines[x + 1][y + 1] == "M")
    ) and (
        (lines[x - 1][y + 1] == "M" and lines[x + 1][y - 1] == "S")
        or (lines[x - 1][y + 1] == "S" and lines[x + 1][y - 1] == "M")
    )


def get_x_positions(lines):
    n = len(lines)

    res = []
    for x in range(1, n - 1):
        for y in range(1, n - 1):
            if lines[x][y] == "A":
                if is_x(lines, x, y):
                    res.append((x, y))
    return res


def display(lines, positions):
    n = len(lines)
    for x in range(n):
        print("".join("X" if (x, y) in positions else "." for y in range(n)))


def resolve2():

    lines = parse_input("input.txt")
    positions = get_x_positions(lines)
    display(lines, positions)
    return len(positions)


if __name__ == "__main__":
    print(resolve1())
    print(resolve2())
