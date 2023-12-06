from functools import reduce
from math import sqrt
from pathlib import Path


def parse_input(path: str):
    p = Path(__file__).resolve().parent / path
    print(p)
    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return content.split("\n")


def win_ways(tmax: int, dmax: int) -> list[int]:
    s1, s2 = polynom_sol(-1, tmax, -dmax)
    assert s1 >= 0
    assert s2 >= 0
    if s1 > s2:
        s1, s2 = s2, s1
    return [t for t in range(int(s1) + 1, int(s2) + 1) if t < s2]


def polynom_sol(a: int, b: int, c: int) -> tuple[float, float]:
    det = pow(b, 2) - 4 * a * c
    return [(-b - sqrt(det)) / (2 * a), (-b + sqrt(det)) / (2 * a)]


def resolve1():
    lines = parse_input("input.txt")
    lines = [[int(t) for t in line.split(":")[1].strip().split()] for line in lines]

    res = [win_ways(tmax, dmax) for tmax, dmax in zip(*lines)]
    return reduce(lambda a, b: a * len(b), res, 1)


def resolve2():
    lines = parse_input("input.txt")
    lines = [[int(t) for t in line.split(":")[1].strip().split()] for line in lines]

    def aggr(numbers: list[int]) -> int:
        return int(reduce(lambda a, b: a + str(b), numbers, ""))

    res = [win_ways(aggr(lines[0]), aggr(lines[1]))]
    return reduce(lambda a, b: a * len(b), res, 1)


if __name__ == "__main__":
    print(resolve1())
    print(resolve2())
