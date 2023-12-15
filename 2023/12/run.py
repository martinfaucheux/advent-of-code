from copy import deepcopy
from dataclasses import dataclass
from functools import cache
from itertools import combinations
from pathlib import Path


@dataclass
class Line:
    record: str
    split_info: list[int]

    def is_valid(self) -> bool:
        if "?" in self.record:
            raise ValueError("Unknown value in record")

        return [len(elt) for elt in self.record.split(".") if elt] == self.split_info

    def get_unknown_indices(self) -> list[int]:
        return [i for i, ltr in enumerate(self.record) if ltr == "?"]

    def get_naive_arrangements(self) -> "list[Line]":
        if "?" not in self.record:
            raise ValueError("No unknown value in record")

        known_count = self.record.count("#")
        total_count = sum(self.split_info)
        unknown_indices = self.get_unknown_indices()

        print(len(unknown_indices), total_count - known_count)

        # get all possible way of picking known_count elt of unknown_indices
        for comb in combinations(unknown_indices, total_count - known_count):
            record = list(self.record.replace("?", "."))
            for idx in comb:
                record[idx] = "#"
            yield Line("".join(record), self.split_info)

    def mult(self, times) -> "Line":
        return Line("?".join([self.record] * times), self.split_info * times)

    def __len__(self) -> int:
        return len(self.record)

    def __repr__(self):
        return f"{self.record} {','.join(str(e) for e in self.split_info)}"

    def __hash__(self):
        return hash(self.record, ",".join(self.split_info))


def parse_input(path: str) -> list[Line]:
    p = Path(__file__).resolve().parent / path
    res = []
    for line in p.read_text().splitlines():
        record, split_info = line.split()
        split_info = [int(i) for i in split_info.split(",")]
        res.append(Line(record, split_info))
    return res


"""
How to do this:
iterate over the chars
keep track of group counts already encountered and wheteher in an actual group

if meet a "?" -> 2 cases
- interpret as . 
- interpret as # 

if meet a #
- if previous was . -> consider it as new group, check if possible


if reach end, check if possible
"""


def get_valid_arangements_still_naive(line: Line):
    if "?" not in line.record:
        raise ValueError("No unknown value in record")

    @dataclass
    class State:
        strl: str
        counters: list[int]

        def get_new(self, s):
            state = deepcopy(self)
            state.strl += s
            return state

    def is_counter_valid(counter, reference, exact=False):
        lcount = len(counter)
        lref = len(reference)

        if lcount == 0:
            return True

        if lref < lcount:
            return False

        if exact:
            return counter[-1] == reference[lcount - 1]

        return counter[-1] <= reference[lcount - 1]

    states = [State("", [])]
    for idx in range(len(line.record)):
        _char = line.record[idx]
        chars = [".", "#"] if _char == "?" else [_char]

        _states = []
        for char in chars:
            for state in states:
                _state = state.get_new(char)

                if char == ".":
                    if state.strl and state.strl[idx - 1] == "#":
                        # end of last group
                        if not is_counter_valid(_state.counters, line.split_info, True):
                            # first groups must match exactly
                            continue

                if char == "#":
                    if (idx == 0) or _state.strl[idx - 1] == ".":
                        # new group
                        _state.counters.append(1)
                    else:
                        _state.counters[-1] += 1

                    # exact check if end of the string
                    if not is_counter_valid(
                        _state.counters, line.split_info, idx == len(line.record) - 1
                    ):
                        continue

                _states.append(_state)

        states = _states

    # if invalid_state := next(
    #     (s for s in states if s.counters != line.split_info), None
    # ):
    #     raise ValueError(f"Invalid state {invalid_state.strl}")

    return [
        Line(state.strl, line.split_info)
        for state in states
        if state.counters == line.split_info
    ]


"""
f(..??..##., (1,2)) = 2 + f(##., (2,))
"""


@cache
def _get_arr_count_rec(record: str, split_info: tuple[int, ...]) -> int:
    record = record.strip(".")

    def repl(_str: str, char: str, idx: int):
        return _str[:idx] + char + _str[idx + 1 :]

    if len(split_info) == 0 and record[:1] != "?":
        return 1 if len(record) == 0 else 0

    if len(record) == 0:
        return 0

    block = record.split(".", 1)[0]
    try:
        unknown_idx = block.index("?")
    except ValueError:
        unknown_idx = None

    if unknown_idx is not None:
        return _get_arr_count_rec(
            repl(record, ".", unknown_idx), split_info
        ) + _get_arr_count_rec(repl(record, "#", unknown_idx), split_info)

    return (
        _get_arr_count_rec(record[len(block) :], split_info[1:])
        if split_info[0] == len(block)
        else 0
    )


def get_arr_count_rec(line: Line):
    return _get_arr_count_rec(line.record, tuple(line.split_info))


def resolve1():
    lines = parse_input("input.txt")
    return sum(
        sum(1 for _line in line.get_naive_arrangements() if _line.is_valid())
        for line in lines
    )


def resolve2():
    lines = parse_input("input.txt")
    return sum(get_arr_count_rec(line.mult(5)) for line in lines)


if __name__ == "__main__":
    print(resolve1())
    print(resolve2())
