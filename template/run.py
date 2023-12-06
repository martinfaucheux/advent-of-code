from pathlib import Path


def parse_input(path: str):
    p = Path(__file__).resolve().parent / path

    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return content.split("\n")


def resolve1():
    lines = parse_input("input_example.txt")

    return 0


def resolve2():
    lines = parse_input("input_example.txt")

    return 0


if __name__ == "__main__":
    print(resolve1())
    print(resolve2())
