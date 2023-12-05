from dataclasses import dataclass


@dataclass
class ConversionRange:
    dest_range_start: int
    source_range_start: int
    range: int

    def convert(self, value: int) -> int | None:
        if self.source_range_start <= value < self.source_range_start + self.range:
            return value - self.source_range_start + self.dest_range_start
        return None


@dataclass
class ConversionMap:
    name: str
    conversions: list[ConversionRange]

    def convert(self, value: int) -> int:
        for conv_range in self.conversions:
            if (conv_value := conv_range.convert(value)) is not None:
                return conv_value
        return value


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

    return seeds, conv_maps


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

    return min(seed_to_location(seed, conv_maps) for seed in seeds)


if __name__ == "__main__":
    print(resolve1())
    print(resolve2())
