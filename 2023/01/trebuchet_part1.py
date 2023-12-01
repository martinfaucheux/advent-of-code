

def get_line_value(line):
    first = next(v for v in line if v.isdigit())
    last = next(v for v in line[::-1] if v.isdigit())
    return int(first + last)


if __name__ == "__main__":
    with open("day1/input.txt") as f:
        lines = f.readlines()

    print( sum(get_line_value(line) for line in lines))