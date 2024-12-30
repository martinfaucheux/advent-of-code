from pathlib import Path
import re

Vect = tuple[int, int]


def parse_input(path: str):
    p = Path(__file__).resolve().parent / path

    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return [Block.from_text(text) for text in content.split("\n\n")]


class Block:
    a: Vect
    b: Vect
    prize_pos: Vect

    def __init__(self, a: Vect, b: Vect, prize_pos: Vect):
        self.a = a
        self.b = b
        self.prize_pos = prize_pos

    def get_pos(self, a: int, b: int) -> Vect:
        x = a * self.a[0] + b * self.b[0]
        y = a * self.a[1] + b * self.b[1]
        return x, y

    @classmethod
    def from_text(cls, text) -> "Block":
        pattern = r"X[\+\=](\d+),\sY[\+\=](\d+)"
        kwargs = {}
        for attr, line in zip(["a", "b", "prize_pos"], text.split("\n")):
            match = re.search(pattern, line)
            kwargs[attr] = (int(match.group(1)), int(match.group(2)))

        return cls(**kwargs)


def get_ordered_combination(limit: int | Vect = 100):
    """
    Iterator for tuples (a, b) such that 0 <= a, b <= limit and
    f(a, b) = a * 3 + b, iterating in non-decreasing order of f(a, b).
    """
    if type(limit) is int:
        a_max = b_max = limit
    else:
        a_max, b_max = limit

    for f_value in range((a_max + 1) * 3 + b_max + 1):
        for a in range(a_max + 1):
            b = f_value - a * 3
            if 0 <= b <= b_max:
                yield a, b


def solve_block(block: Block, prize_offset: Vect = (0, 0)) -> Vect | None:
    prize_pos = (
        block.prize_pos[0] + prize_offset[0],
        block.prize_pos[1] + prize_offset[1],
    )

    a_max = min(prize_pos[i] // block.a[i] for i in (0, 1))
    b_max = min(prize_pos[i] // block.b[i] for i in (0, 1))

    for a, b in get_ordered_combination((a_max, b_max)):

        if (a == 80) and (b == 40):
            pass
        pos = block.get_pos(a, b)
        if pos == prize_pos:
            return a, b
    return None


def get_cost(a, b):
    return a * 3 + b


def compute_gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return abs(a)


def euclid_extended(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        return a, 1, 0

    gcd, u1, v1 = euclid_extended(b, a % b)

    u = v1
    v = u1 - (a // b) * v1

    return gcd, u, v


def solve_linear_diophantine(a: int, b: int, d: int) -> tuple[int, int, int]:
    gcd, u0, v0 = euclid_extended(a, b)
    if d % gcd != 0:
        raise ValueError("Eq has no solution")

    # adapt for constant d
    k = d // gcd
    u = u0 * k
    v = v0 * k

    return u, v, gcd


def has_solution(block: Block, prize_pos: Vect) -> bool:
    return all(
        (prize_pos[i] % compute_gcd(block.a[i], block.b[i]) == 0) for i in (0, 1)
    )


def solve_diophantine(a, b, p) -> set[Vect]:
    gcd = compute_gcd(a, b)
    if p % gcd != 0:
        return set()

    _, u, v = euclid_extended(a, b)


def resolve1():
    blocks = parse_input("input.txt")
    cost = 0
    for block in blocks:
        res = solve_block(block)
        if res is not None:
            cost += get_cost(*res)

    return cost


def add_vect(a: Vect, b: Vect) -> Vect:
    return (a[0] + b[0], a[1] + b[1])


def resolve2():
    blocks = parse_input("input_example.txt")
    k = 10000000000000
    cost = 0
    for block in blocks:
        if has_solution(block, add_vect(block.prize_pos, (k, k))):

            res = solve_block(block, (k, k))
            if res is not None:
                cost += get_cost(*res)

            break

    return cost


if __name__ == "__main__":
    # print(resolve1())
    print(resolve2())
