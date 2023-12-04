def resolve2() -> int:
    with open("2023/03/input.txt") as f:
        input_str = f.read().splitlines()

    # print(list(get_cog_pair_values(input_str)))
    print(sum(ratio[0] * ratio[1] for ratio in get_cog_pair_values(input_str)))


def get_cog_pair_values(code: list[str]):
    res = []
    for cog_pos in get_cog_pos(code):
        numbers = get_surrounding_numbers(code, cog_pos)
        if len(numbers) == 2:
            res.append(numbers)
    return res


def get_surrounding_numbers(code: list[str], cog_pos: tuple[int, int]):
    positions = get_neighbor_positions(code, *cog_pos)
    numbers = []
    visited = []
    for pos in positions:
        if pos in visited:
            continue

        line_idx, start_idx = pos
        if code[line_idx][start_idx].isdigit():
            end_idx = start_idx + 1
            visited.append((line_idx, end_idx))

            while end_idx < len(code[0]) and code[line_idx][end_idx].isdigit():
                end_idx += 1
                visited.append((line_idx, end_idx))

            while start_idx - 1 >= 0 and code[line_idx][start_idx - 1].isdigit():
                start_idx -= 1
                visited.append((line_idx, start_idx))

            numbers.append(int(code[line_idx][start_idx:end_idx]))

    return numbers


def get_cog_pos(code: list[str]) -> list[tuple[int, int]]:
    res = []
    for line_idx, line in enumerate(code):
        for char_idx, char in enumerate(line):
            if char == "*":
                res.append((line_idx, char_idx))
    return res


def get_neighbor_positions(
    code: list[str], line_idx: int, char_idx: int
) -> list[tuple[int, int]]:
    return [
        (x, y)
        for x in range(line_idx - 1, line_idx + 2)
        for y in range(char_idx - 1, char_idx + 2)
        if (0 <= x < len(code) and 0 <= y < len(code[0]) and not (x == 0 and y == 0))
    ]


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
    print(resolve2())
