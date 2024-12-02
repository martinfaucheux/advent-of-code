from pathlib import Path


def parse_input(path: str):
    p = Path(__file__).resolve().parent / path

    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return [[int(elt) for elt in line.split(" ")] for line in content.split("\n")]


def resolve1():
    lines = parse_input("input.txt")
    return sum((1 if check_line(line) else 0) for line in lines)


def check_line(line: list[int]) -> bool:
    diff = [a - b for a, b in zip(line[1:], line[:-1])]
    return all((elt >= 1 and elt <= 3) for elt in diff) or all(
        (elt <= -1 and elt >= -3) for elt in diff
    )


def get_sublines(line: list[int]) -> list[list[int]]:
    return [line] + [line[:i] + line[i + 1 :] for i in range(len(line))]


def resolve2():
    lines = parse_input("input.txt")
    return sum(
        (1 if any(check_line(subline) for subline in get_sublines(line)) else 0)
        for line in lines
    )


if __name__ == "__main__":
    print(resolve1())
    print(resolve2())
