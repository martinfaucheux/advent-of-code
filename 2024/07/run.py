from pathlib import Path

OPERATIONS = "+*"


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


def get_bin(_int: int, padding: int | None = None) -> str:
    res = bin(_int)[2:]

    if padding is not None:
        res = "0" * (padding - len(res)) + res

    return res


def is_valid_equation(exp_res: int, operands: list[int]) -> bool:
    operator_count = len(operands) - 1

    for option in range(2**operator_count):
        if process_line(operands, get_bin(option, operator_count)) == exp_res:
            return True
    return False


def process_line(operands: list[int], op_mask: str) -> int:
    print(op_mask)
    res = operands[0]
    for b, operand in zip(op_mask, operands[1:]):
        if b == "0":
            res *= operand
        elif b == "1":
            res += operand
        else:
            raise ValueError(f"invalid value {b}")
    return res


def resolve1():
    lines = parse_input("input.txt")

    res = 0
    for exp_res, operands in lines:
        print(exp_res, operands)
        if is_valid_equation(exp_res, operands):
            res += exp_res

    return res


def resolve2():
    lines = parse_input("input_example.txt")

    return 0


if __name__ == "__main__":
    print(resolve1())
    print(resolve2())
