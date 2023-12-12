from pathlib import Path


def parse_input(path: str):
    p = Path(__file__).resolve().parent / path
    return [[int(elt) for elt in l.split()] for l in p.read_text().splitlines()]


def resolve1():
    lines = parse_input("input.txt")
    return sum(get_prediction(line) for line in lines)


def resolve2():
    lines = parse_input("input.txt")
    return sum(get_back_prediction(line) for line in lines)


def get_prediction(line: list[int]) -> int:
    assert isinstance(line, list), line
    table = [line]

    while not all(elt == 0 for elt in table[-1]):
        table.append(reduce_line(table[-1]))

    return sum(line[-1] for line in table)


def get_back_prediction(line: list[int]) -> int:
    assert isinstance(line, list), line
    table = [line]

    while not all(elt == 0 for elt in table[-1]):
        table.append(reduce_line(table[-1]))

    res = 0
    for idx in range(len(table) - 1, -1, -1):
        res = table[idx][0] - res

    return res


def reduce_line(line: list[int]) -> list[int]:
    return [line[idx + 1] - elt for idx, elt in enumerate(line[:-1])]


if __name__ == "__main__":
    print(resolve1())
    print(resolve2())
