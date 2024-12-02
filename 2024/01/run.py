from pathlib import Path
import re


def parse_input(path: str):
    p = Path(__file__).resolve().parent / path

    pattern = r"(\d+)\s+(\d+)"

    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return [
        (int(a), int(b))
        for line in content.split("\n")
        for a, b in re.findall(pattern, line)
    ]


def resolve1():
    lines = parse_input("input.txt")
    transposed = [list(sorted(row)) for row in zip(*lines)]
    return sum(abs(a - b) for a, b in zip(*transposed))


def resolve2():
    lines = parse_input("input.txt")
    transposed = [list(sorted(row)) for row in zip(*lines)]

    occ_map = {k: 0 for k in transposed[0]}
    for elt in transposed[1]:
        if elt in occ_map:
            occ_map[elt] += 1

    return sum(elt * occ_map[elt] for elt in transposed[0])


if __name__ == "__main__":
    print(resolve1())
    print(resolve2())
