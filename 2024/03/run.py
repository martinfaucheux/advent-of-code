from pathlib import Path


import re

MUL_PATTERN = r"mul\((\d{1,3}),(\d{1,3})\)"
DO_PATTERN = r"do\(\)"
DONT_PATTERN = r"don't\(\)"


def parse_input(path: str):
    p = Path(__file__).resolve().parent / path

    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return content


def resolve1():
    line = parse_input("input.txt")
    matches = re.findall(MUL_PATTERN, line)
    return sum(int(left) * int(right) for left, right in matches)


def resolve2():
    line = parse_input("input.txt")
    res = 0
    enable = True
    _debug = []
    while line:
        for pattern in [DO_PATTERN, DONT_PATTERN, MUL_PATTERN]:
            if (_match := re.match("^" + pattern, line)) is not None:
                if pattern == DO_PATTERN:
                    enable = True
                elif pattern == DONT_PATTERN:
                    enable = False
                elif pattern == MUL_PATTERN:
                    if enable:
                        left, right = _match.groups()
                        res += int(left) * int(right)
                match_str = _match.group(0)
                _debug.append(match_str)
                line = line[len(match_str) :]
                break
        else:
            line = line[1:]

    print(_debug)
    return res


if __name__ == "__main__":
    print(resolve1())
    print(resolve2())
