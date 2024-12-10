from pathlib import Path
from uuid import uuid4


def parse_input(path: str) -> str:
    p = Path(__file__).resolve().parent / path

    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]
    return content


def to_array(line: str) -> list[int]:
    res = []
    block_id = 0
    is_file = True
    for block_length in line:
        block_length = int(block_length)

        if is_file:
            res += [block_id] * block_length
            block_id += 1
        else:
            res += [-1] * block_length

        is_file = not is_file

    return res


def solve_p1(array: list[int]) -> list[int]:
    array = array[:]
    inc_cursor = 0
    dec_cursor = len(array) - 1

    while inc_cursor <= dec_cursor:
        if array[inc_cursor] != -1:
            inc_cursor += 1
            continue
        if (value := array[dec_cursor]) == -1:
            dec_cursor -= 1
            continue

        array[dec_cursor] = -1
        array[inc_cursor] = value
        inc_cursor += 1
    return array


def display(array):
    print("".join(("." if elt == -1 else str(elt)) for elt in array))


def resolve1():
    line = parse_input("input.txt")
    array = to_array(line)
    solved = solve_p1(array)
    # display(solved)
    return sum(i * v for i, v in enumerate(solved) if v != -1)


class Block:
    size: int
    _uuid: uuid4
    id: int | None = None

    def __init__(self, size: int, id: int | None = None):
        self.size = size
        self.id = id
        self._uuid = uuid4()

    @property
    def is_empty(self):
        return self.id is None

    def __hash__(self):
        return hash(self._uuid)

    def __repr__(self):
        return f"({'X' if self.is_empty else self.id }, {self.size})"

    def __eq__(self, other):
        return self.size == other.size and self.id == other.id


def line_to_blocks(line: str) -> list[Block]:
    res = []
    is_empty = False
    index = 0
    for count in line:
        count = int(count)
        if not is_empty:
            if count > 0:
                res.append(Block(id=index, size=count))
            index += 1
        else:
            if count > 0:
                res.append(Block(id=None, size=count))
        is_empty = not is_empty
    return res


def reorder_blocks(blocks):
    blocks = blocks[:]
    seen = set()

    length = sum(block.size for block in blocks)

    file_block_idx = len(blocks) - 1
    while file_block_idx > 1:
        # for file_block_idx in range(len(blocks) - 1, -1, -1):
        file_block = blocks[file_block_idx]
        if file_block.is_empty or file_block in seen:
            file_block_idx -= 1
            continue

        found = False

        for empty_block_idx, empty_block in enumerate(blocks):
            if empty_block_idx >= file_block_idx:
                break
            if empty_block.is_empty and empty_block.size >= file_block.size:
                found = True
                break

        seen.add(file_block)

        if found:
            # print(
            #     f"insert {file_block} (idx {file_block_idx}) at {empty_block} (idx {empty_block_idx})"
            # )

            del blocks[file_block_idx]
            blocks.insert(file_block_idx, Block(id=None, size=file_block.size))
            check_size(blocks, length)
            blocks = consolidate(blocks, file_block_idx)
            check_size(blocks, length)

            blocks.insert(empty_block_idx, file_block)
            # empty_block.size = size_diff
            assert blocks[empty_block_idx + 1].is_empty
            blocks[empty_block_idx + 1].size -= file_block.size
            check_size(blocks, length)
            blocks = consolidate(blocks, empty_block_idx + 1)
            check_size(blocks, length)
        else:
            file_block_idx -= 1

    return blocks


def check_size(blocks: list[Block], exp_size: int) -> None:
    size = sum(block.size for block in blocks)
    assert size == exp_size, f"the line length changed ({size} != {exp_size})"


def consolidate(blocks: list[Block], index: int):
    if not blocks[index].is_empty:
        return blocks
    start, end = index, index + 1
    size = blocks[index].size
    if index > 0 and blocks[index - 1].is_empty:
        start -= 1
        size += blocks[index - 1].size

    if (index < len(blocks) - 1) and blocks[index + 1].is_empty:
        end += 1
        size += blocks[index + 1].size

    blocks = blocks[:start] + [Block(id=None, size=size)] + blocks[end:]
    return blocks


def get_checksum(blocks: list[Block]) -> int:
    idx_acc = 0
    checksum = 0
    for block in blocks:
        if not block.is_empty:
            checksum += sum(
                block.id * idx for idx in range(idx_acc, idx_acc + block.size)
            )
        idx_acc += block.size
    return checksum


def flat_repr(blocks: list[Block]) -> str:
    res = ""
    for block in blocks:
        res += ("." if block.is_empty else str(block.id)) * block.size
    return res


def display_blocks(blocks: list[Block]) -> None:
    print(flat_repr(blocks))


def _resolve2(path: str):

    line = parse_input(path)
    print(line)
    blocks = line_to_blocks(line)
    display_blocks(blocks)
    blocks = reorder_blocks(blocks)
    return get_checksum(blocks)


def test() -> None:
    p = Path(__file__).resolve().parent / "test_cases.txt"

    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]

    sections = content.split("\n\n")
    for test_id, section in enumerate(sections):
        print(f"test {test_id+1}")
        _input, exp_repr, exp_output = section.split("\n")
        blocks = line_to_blocks(_input)
        repr = flat_repr(blocks)
        print(repr)
        assert repr == exp_repr

        blocks = reorder_blocks(blocks)
        output_repr = flat_repr(blocks)
        assert output_repr == exp_output, f"{output_repr} != {exp_output}"


def resolve2():
    test()
    return _resolve2("input.txt")


if __name__ == "__main__":
    print(resolve2())
