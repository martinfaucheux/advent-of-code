import math
import re
from functools import reduce
from pathlib import Path

Map = dict[str, tuple[str, str]]


def parse_input(path: str):
    p = Path(__file__).resolve().parent / path

    instr, lines = p.read_text().split("\n\n")

    # capture AAA = (BBB, CCC)
    pattern = r"(\w+) = \((\w+), (\w+)\)"
    _map = {}
    for line in lines.splitlines():
        m = re.match(pattern, line)
        if m:
            _map[m.group(1)] = (m.group(2), m.group(3))

    return instr, _map


def incr_step(_map: Map, instr: str, step: int, place: str) -> str:
    match (instr[step % len(instr)]):
        case "L":
            idx = 0
        case "R":
            idx = 1
        case _:
            raise ValueError("Invalid instruction")

    return _map[place][idx]


def count_steps(instr, _map):
    count = 0
    place = "AAA"
    while True:
        if place == "ZZZ":
            return count
        place = incr_step(_map, instr, count, place)
        count += 1


def resolve1():
    instr, _map = parse_input("input.txt")

    return count_steps(instr, _map)


def resolve2():
    instr, _map = parse_input("input_example2.txt")
    places = [place for place in _map if place[-1] == "A"]
    step = 0
    while True:
        if all(place[-1] == "Z" for place in places):
            return step

        places = [incr_step(_map, instr, step, place) for place in places]
        step += 1


def lcm(numbers):
    return reduce(math.lcm, numbers, 1)


def draw(map):
    """
    stateDiagram-v2
        [*] --> Still
        Still --> [*]
        Still --> Moving
        Moving --> Still
        Moving --> Crash
        Crash --> [*]
    """
    lines = [
        "stateDiagram-v2",
        "\tclassDef START fill:red",
        "\tclassDef END fill:green",
    ]
    for k, (l, r) in map.items():
        lines.append(f"\t{k} --> {l} : L")
        lines.append(f"\t{k} --> {r} : R")

        if k[-1] == "A":
            lines.append(f"\tclass {k} START")

        if k[-1] == "Z":
            lines.append(f"\tclass {k} END")
    graph = "\n".join(lines)

    p = Path(__file__).resolve().parent / "graph.mermaid"
    p.write_text(graph)


def find_periods():
    instr, _map = parse_input("input.txt")
    draw(_map)
    places = [place for place in _map if place[-1] == "A"]
    l_instr = len(instr)

    res = []
    for place in places:
        step = 0
        recorded_pos = []
        found_idx = None
        min_match_idx = -1
        while True:
            pos = (place, step % l_instr)

            if place[-1] == "Z":
                try:
                    found_idx = recorded_pos.index(pos)
                except ValueError:
                    recorded_pos.append(pos)

                if found_idx is not None:
                    break

                if min_match_idx == -1:
                    min_match_idx = step

            place = incr_step(_map, instr, step, place)
            step += 1

        period = step - min_match_idx
        min_match_idx = min_match_idx % period
        res.append((min_match_idx, period))
    return res


def resolve2_better():
    congruences = find_periods()

    return math.lcm(*[c[1] for c in congruences])


if __name__ == "__main__":
    print(resolve1())
    # print(resolve2())
    print(resolve2_better())
