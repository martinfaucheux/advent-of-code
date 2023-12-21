import re
from copy import deepcopy
from dataclasses import dataclass
from functools import reduce
from math import inf
from pathlib import Path
from queue import Queue

LETTERS = "xmas"


@dataclass
class Rule:
    target: str
    operator: str = "default"
    letter: str | None = None
    value: int = 0

    def compute(self, input) -> str | None:
        if (
            self.operator == "default"
            or (self.operator == "<" and input[self.letter] < self.value)
            or (self.operator == ">" and input[self.letter] > self.value)
        ):
            return self.target

        return None


@dataclass
class Workflow:
    rules: list[Rule]

    def process(self, input: dict):
        for rule in self.rules:
            if (target := rule.compute(input)) is not None:
                return target

        raise ValueError(f"No matching rule")


def parse_input(path: str):
    p = Path(__file__).resolve().parent / path
    workflow_str, input_str = p.read_text().split("\n\n")

    workflows = {}
    for line in workflow_str.splitlines():
        name, rules = read_workflow(line)
        workflows[name] = rules

    return workflows, [read_part(inp) for inp in input_str.splitlines()]


def read_workflow(line: str) -> tuple[str, list[Rule]]:
    match = re.match(r"([a-z]+)\{(.+)\}", line)
    name, rule_strings = match.groups()
    rules = []
    rule_strings = rule_strings.split(",")
    for rule_str in rule_strings[:-1]:
        match = re.match(r"([a-z])(<|>)(\d+):([a-z]+|[A-Z])", rule_str)
        letter, op, value, target = match.groups()
        rules.append(
            Rule(letter=letter, operator=op, value=int("".join(value)), target=target)
        )
    rules.append(Rule(target=rule_strings[-1], operator="default"))
    return name, Workflow(rules)


def read_part(line: str):
    """
    "{x=787,m=2655,a=1222,s=2876}"
    returns {"x": 787, "m": 2655, "a": 1222, "s": 2876}
    """
    return {
        (sp := instr.split("="))[0]: int(sp[1])
        for instr in line.strip("\{\}").split(",")
    }


def process(workflows: dict[str, Workflow], input: dict[str, int]) -> bool:
    # get first key of workflow
    label = "in"
    while label not in ["A", "R"]:
        label = workflows[label].process(input)
        # print(label)

    return label == "A"


def resolve1():
    workflows, part_inputs = parse_input("input.txt")

    return sum(
        sum(part_input.values())
        for part_input in part_inputs
        if process(workflows, part_input)
    )


class Interval:
    _min: int
    _max: int

    def __init__(self, _min: int | None = None, _max: int | None = None):
        self._min = _min if _min is not None else -inf
        self._max = _max if _max is not None else inf

    def split(self, value):
        return Interval(self._min, value - 1), Interval(value, self._max)

    @property
    def content_sum(self):
        if self._min == -inf or self._max == inf:
            raise ValueError("Infinite sum!")
        return max(0, self._max - self._min + 1)

    def __hash__(self):
        return hash((self._min, self._max))

    def __bool__(self) -> bool:
        return self._min < self._max

    def __repr__(self):
        return str((self._min, self._max))


class MetaInterval:
    _dict: dict[str, Interval]

    def __init__(self):
        self._dict = {k: Interval(1, 4000) for k in LETTERS}

    def split(self, value: int, letter: str):
        lower, greater = self[letter].split(value)
        meta_lower, meta_greater = deepcopy(self), deepcopy(self)
        meta_lower[letter] = lower
        meta_greater[letter] = greater
        return meta_lower, meta_greater

    @property
    def content_sum(self):
        return reduce(lambda acc, i: acc * i.content_sum, self._dict.values(), 1)

    def __hash__(self):
        return hash(tuple(self._dict[l] for l in LETTERS))

    def __getitem__(self, letter: str):
        if letter not in LETTERS:
            raise KeyError(f"Invalid letter: {letter}")
        return self._dict[letter]

    def __setitem__(self, letter: str, interval: Interval):
        if letter not in LETTERS:
            raise KeyError(f"Invalid letter: {letter}")
        self._dict[letter] = interval

    def __bool__(self) -> bool:
        return all(bool(interval) for interval in self._dict.values())

    def __repr__(self):
        return str(self._dict)


def split_intervals(workflows: dict[str, Workflow]):
    q = Queue()
    q.put((MetaInterval(), "in", 0))

    valid_intervales: set[MetaInterval] = set()
    while not q.empty():
        interval, label, rule_idx = q.get()
        workflow = workflows[label]
        rule = workflow.rules[rule_idx]

        if rule.operator != "default":
            if rule.operator == "<":
                interval, new_interval = interval.split(rule.value, rule.letter)
            else:
                new_interval, interval = interval.split(rule.value + 1, rule.letter)

            if new_interval:
                q.put((new_interval, label, rule_idx + 1))

        if interval:
            next_label = rule.target
            match next_label:
                case "A":
                    valid_intervales.add(interval)
                case "R":
                    pass
                case _:
                    q.put((interval, next_label, 0))

    return valid_intervales


if __name__ == "__main__":
    # print(resolve2())

    workflows, _ = parse_input("input.txt")
    intervals = split_intervals(workflows)
    from pprint import pprint

    pprint(intervals)
    res = sum(interval.content_sum for interval in intervals)
    print(res)

    # interval = MetaInterval()
    # interval, _ = interval.split(7, "s")

    # _, interval = interval.split(8, "s")
    # print(bool(interval))
