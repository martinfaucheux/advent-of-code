from pathlib import Path
from functools import lru_cache, cache


def parse_input(path: str) -> list[int]:
    p = Path(__file__).resolve().parent / path

    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return [int(elt) for elt in content.split(" ")]


def count_digits(number: int) -> str:
    return len(str(number))


def process_line(line: list[int]):
    next_line = []
    for elt in line:
        n1, n2 = process_number(elt)
        next_line.append(n1)
        if n2 is not None:
            next_line.append(n2)
    return next_line


@lru_cache
def process_number(n: int) -> tuple[int, int | None]:
    if n == 0:
        return (1, None)
    elif (digit_count := count_digits(n)) % 2 == 0:
        divider = 10 ** (digit_count // 2)
        return (n // divider, n % divider)
    else:
        return (n * 2024, None)


@cache
def rec(n: int, counter: int) -> int:
    if n == 0:
        res = [1]
    elif (digit_count := count_digits(n)) % 2 == 0:
        divider = 10 ** (digit_count // 2)
        res = [n // divider, n % divider]
    else:
        res = [n * 2024]

    if counter == 0:
        return len(res)
    else:
        return sum(rec(elt, counter - 1) for elt in res)


def resolve1():

    line = parse_input("input.txt")
    count = 25
    res = 0
    for i_elt, elt in enumerate(line):
        res += rec(elt, count - 1)

    return res


def resolve2():
    line = parse_input("input.txt")
    count = 75
    res = 0
    for i_elt, elt in enumerate(line):
        res += rec(elt, count - 1)

    return res


if __name__ == "__main__":
    print(resolve1())
    print(resolve2())
