from dataclasses import dataclass

import math
import time
from datetime import timedelta
from functools import lru_cache


# START_IDX = 0
# START_SEED = 1247895974
# MIN_VAL = 393472033
# SPENT_DURATION = 699.8467710018158


@dataclass
class ConversionRange:
    dest_range_start: int
    source_range_start: int
    range: int

    def convert(self, value: int) -> int | None:
        if self.source_range_start <= value < self.source_range_start + self.range:
            return value - self.source_range_start + self.dest_range_start
        return None

    def __hash__(self):
        return hash((self.dest_range_start, self.source_range_start, self.range))


@dataclass
class ConversionMap:
    name: str
    conversions: list[ConversionRange]

    def convert(self, value: int) -> int:
        for conv_range in self.conversions:
            if (conv_value := conv_range.convert(value)) is not None:
                return conv_value
        return value

    def __hash__(self):
        return hash(self.name)


# @lru_cache(maxsize=128)
def seed_to_location(seed: int, conv_maps: list[ConversionMap]) -> int:
    for conv_map in conv_maps:
        seed = conv_map.convert(seed)
    return seed


def parse_data(input_str: str) -> tuple[list[int], list[ConversionMap]]:
    seed_block, *conv_blocks = input_str.split("\n\n")

    seeds = [int(seed) for seed in seed_block.split(": ", 1)[1].split()]
    conv_maps = []
    for conv_block in conv_blocks:
        name_line, *conv_lines = conv_block.split("\n")
        name = name_line.split(maxsplit=1)[0]
        conv_ranges = []
        for conv_line in conv_lines:
            values = conv_line.split()
            assert len(values) == 3, values
            a, b, c = values
            conv_ranges.append(ConversionRange(int(a), int(b), int(c)))

        conv_maps.append(ConversionMap(conversions=conv_ranges, name=name))

    return seeds, tuple(conv_maps)


def resolve1():
    with open("2023/05/input.txt") as f:
        input_str = f.read()

    seeds, conv_maps = parse_data(input_str)
    return min(seed_to_location(seed, conv_maps) for seed in seeds)


def resolve2():
    with open("2023/05/input.txt") as f:
        input_str = f.read()

    seed_data, conv_maps = parse_data(input_str)

    seeds = (
        seed
        for idx in range(0, len(seed_data) // 2)
        for seed in range(
            seed_data[idx * 2], seed_data[idx * 2] + seed_data[idx * 2 + 1]
        )
    )

    seed_count = sum(seed_data[idx * 2 + 1] for idx in range(len(seed_data) // 2))

    op_count = 0
    start_time = time.time()
    try:
        min_val = math.inf
        for _idx in list(range(len(seed_data) // 2)):
            start_seed = seed_data[_idx * 2]
            seed_range = seed_data[_idx * 2 + 1]
            for seed in range(start_seed, start_seed + seed_range):
                val = seed_to_location(seed, conv_maps)
                min_val = min(val, min_val)
                op_count += 1

                if op_count % 1_000_000 == 0:
                    ratio = op_count / seed_count
                    eta = (time.time() - start_time) / ratio
                    eta_str = str(timedelta(seconds=int(eta)))

                    print(
                        f"op_count: {op_count},\tpercent: {ratio * 100:.2f}%\tETA: {eta_str}"
                    )

    except KeyboardInterrupt:
        print(
            f"idx: {_idx}, seed: {seed}, min_val: {min_val}, duration: {str(timedelta(seconds=time.time() - start_time))}"
        )

    return min_val
    # return sum(1 for _ in seeds)
    # return min(seed_to_location(seed, conv_maps) for seed in seeds)


if __name__ == "__main__":
    # print(resolve1())
    print(resolve2())
