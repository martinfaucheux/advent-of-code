DIGIT_MAP = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def get_line_value(line, rev=False):
    for idx in range(len(line)):
        if rev:
            idx = len(line) - idx - 1
        char = line[idx]

        if char.isdigit():
            return char

        for digit_str, digit_int in DIGIT_MAP.items():
            if line[idx:].startswith(digit_str):
                return str(digit_int)


def get_line_values(line):
    first = get_line_value(line)
    last = get_line_value(line, True)
    res = int(first + last)
    return res


if __name__ == "__main__":
    with open("2023/01/input.txt") as f:
        lines = f.readlines()

    print(sum(get_line_values(line) for line in lines))
