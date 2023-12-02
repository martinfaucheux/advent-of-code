from dataclasses import dataclass
from functools import reduce

COLORS = ["red", "green", "blue"]

# only 12 red cubes, 13 green cubes, and 14 blue cubes
MAX_DATA = {"red": 12, "green": 13, "blue": 14}


def max_cubeset(a, b):
    return CubeSet(
        red=max(a.red, b.red),
        blue=max(a.blue, b.blue),
        green=max(a.green, b.green),
    )


@dataclass
class CubeSet:
    red: int = 0
    blue: int = 0
    green: int = 0

    @staticmethod
    def from_dict(data: dict[str, int]) -> "CubeSet":
        return CubeSet(
            red=data.get("red", 0),
            blue=data.get("blue", 0),
            green=data.get("green", 0),
        )

    @property
    def is_valid(self) -> bool:
        return (
            self.red <= MAX_DATA["red"]
            and self.blue <= MAX_DATA["blue"]
            and self.green <= MAX_DATA["green"]
        )

    @property
    def power(self) -> int:
        return self.red * self.blue * self.green


def parse_line(line: str) -> list[CubeSet]:
    res = []
    for subgame in line.split(": ", 1)[-1].split("; "):
        subgame_data = {}
        for color_data in subgame.split(", "):
            number, color = color_data.split(" ", 1)
            assert number.isdigit(), f"invalid number: {number}"
            assert color in COLORS, f"invalid color: {color}"
            subgame_data[color] = int(number)
        res.append(CubeSet.from_dict(subgame_data))
    return res


def is_game_valid(game: list[dict[str, int]]) -> bool:
    return all(subgame.is_valid for subgame in game)


def resolve_part1():
    with open("2023/02/input.txt") as f:
        input_data = f.read()
    games = [parse_line(line) for line in input_data.splitlines()]

    return sum(idx + 1 for idx, game in enumerate(games) if is_game_valid(game))


def resolve_part2():
    with open("2023/02/input.txt") as f:
        input_data = f.read()

    games = [parse_line(line) for line in input_data.splitlines()]

    return sum(
        reduce(max_cubeset, (cubeset for cubeset in game), CubeSet()).power
        for game in games
    )


if __name__ == "__main__":
    print(resolve_part1())
    print(resolve_part2())
