from pathlib import Path
from typing import Callable
import operator

Operation = Callable[[int, int], int]


def parse_input(path: str):
    p = Path(__file__).resolve().parent / path

    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return [
        (int(_split[0]), [int(elt) for elt in _split[1].split(" ")])
        for line in content.split("\n")
        if (_split := line.split(": "))
    ]


def get_base_notation(number: int, base: int = 2) -> list[int]:
    if number == 0:
        return []

    result = []
    is_negative = number < 0
    number = abs(number)

    while number > 0:
        result = [number % base] + result
        number //= base

    if is_negative:
        result = "-" + result

    return result


def get_base_notation_with_padding(number: int, base: int, padding: int) -> list[int]:
    res = get_base_notation(number, base)
    return [0] * (padding - len(res)) + res


def is_valid_equation(
    exp_res: int, operands: list[int], operations: list[Operation]
) -> bool:
    operator_count = len(operands) - 1
    base = len(operations)

    for option in range(base**operator_count):
        if (
            process_line(
                operands,
                get_base_notation_with_padding(option, base, operator_count),
                operations,
            )
            == exp_res
        ):
            return True
    return False


def process_line(
    operands: list[int], op_mask: list[int], operations: list[Operation]
) -> int:
    res = operands[0]
    for op_id, operand in zip(op_mask, operands[1:]):
        op = operations[op_id]
        res = op(res, operand)
    return res


def concatenate(a: int, b: int) -> int:
    return int(str(a) + str(b))


def resolve1():
    lines = parse_input("input.txt")

    operations = [operator.add, operator.mul]

    res = 0
    for exp_res, operands in lines:
        if is_valid_equation(exp_res, operands, operations):
            res += exp_res

    return res


def resolve2():
    lines = parse_input("input.txt")

    operations = [operator.add, operator.mul, concatenate]

    res = 0
    for exp_res, operands in lines:
        if is_valid_equation(exp_res, operands, operations):
            res += exp_res

    return res


if __name__ == "__main__":
    print(resolve1())
    print(resolve2())
