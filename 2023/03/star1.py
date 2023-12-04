def resolve1() -> int:
    with open("2023/03/input.txt") as f:
        input_str = f.read().splitlines()

    numbers = find_numbers(input_str)
    print(numbers)
    return sum(numbers)


def find_numbers(code: list[str]) -> list[int]:
    line_len = len(code[0])
    res = []
    for line_idx, line in enumerate(code):
        start_idx = 0
        while start_idx < line_len:
            if line[start_idx].isdigit():
                end_idx = start_idx + 1
                while end_idx < line_len and line[end_idx].isdigit():
                    end_idx += 1

                if is_part_number(code, line_idx, start_idx, end_idx):
                    res.append(int(line[start_idx:end_idx]))

                start_idx = end_idx
            else:
                start_idx += 1
    return res


def is_part_number(
    code: list[str], line_idx: str, start_idx: int, end_idx: int
) -> bool:
    return (
        any(
            is_special_character(code, line_idx - 1, char_idx)
            for char_idx in range(start_idx - 1, end_idx + 1)
        )
        or any(
            is_special_character(code, line_idx + 1, char_idx)
            for char_idx in range(start_idx - 1, end_idx + 1)
        )
        or is_special_character(code, line_idx, start_idx - 1)
        or is_special_character(code, line_idx, end_idx)
    )


def is_special_character(code: list[str], line_idx: int, char_idx):
    if 0 <= line_idx < len(code) and 0 <= char_idx < len(code[0]):
        char = code[line_idx][char_idx]
        return not char.isdigit() and char != "."
    return False


if __name__ == "__main__":
    print(resolve1())
