from collections import OrderedDict
from pathlib import Path


def parse_input(path: str):
    p = Path(__file__).resolve().parent / path
    return p.read_text().strip().split(",")


def _convert(_str, acc):
    if not _str:
        return acc

    value = (acc + ord(_str[0])) * 17 % 256
    return _convert(_str[1:], value)


def convert(_str):
    return _convert(_str, 0)


"""
Determine the ASCII code for the current character of the string.
Increase the current value by the ASCII code you just determined.
Set the current value to itself multiplied by 17.
Set the current value to the remainder of dividing itself by 256.
"""


def test():
    assert convert("rn=1") == 30
    assert convert("cm-") == 253
    assert convert("qp=3") == 97
    assert convert("cm=2") == 47
    assert convert("qp-") == 14
    assert convert("pc=4") == 180
    assert convert("ot=9") == 9
    assert convert("ab=5") == 197
    assert convert("pc-") == 48
    assert convert("pc=6") == 214
    assert convert("ot=7") == 231


def resolve1():
    lines = parse_input("input.txt")
    for line in lines:
        print(line, convert(line))
    return sum(convert(line) for line in lines)


def resolve2():
    steps = parse_input("input.txt")
    state = [OrderedDict() for _ in range(256)]
    """
    [
        {"rn": 1, "cm": 2},
        {"ot": 7, "ab": 5, "pc": 6},
    ]
    """

    for instr in steps:
        if len(split := instr.split("=", 1)) == 2:
            label, value = split
            num = convert(label)

            # try:
            #     del state[num][label]
            # except KeyError:
            #     pass

            state[num][label] = int(value)

        elif instr[-1] == "-":
            label = instr[:-1]
            num = convert(label)

            try:
                del state[num][label]
            except KeyError:
                pass
        else:
            raise ValueError(f"Invalid instr: {instr}")

    return state


def get_value(state: list[OrderedDict[str, int]]):
    res = 0
    for box_idx, box in enumerate(state):
        for slot_idx, value in enumerate(box.values()):
            res += (box_idx + 1) * (slot_idx + 1) * value
    return res


if __name__ == "__main__":
    test()
    # print(resolve1())
    state = resolve2()
    print(get_value(state))
