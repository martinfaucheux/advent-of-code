from pathlib import Path

from collections import defaultdict
from functools import partial, cmp_to_key

# if there no cycle, we might be able to associate a weight to each number and use it for ordering the list


def parse_input(path: str):
    p = Path(__file__).resolve().parent / path

    content = p.read_text()
    if content.endswith("\n"):
        content = content[:-1]

    section1, section2 = content.split("\n\n")
    ordering_rules = [
        tuple(int(elt) for elt in line.split("|")) for line in section1.split()
    ]
    instr_list = [
        [int(elt) for elt in line.split(",")] for line in section2.split("\n")
    ]

    return ordering_rules, instr_list


def get_rule_map(rule_list: list[tuple[int, int]]) -> dict[int, set[int]]:
    res = defaultdict(set)
    for a, b in rule_list:
        res[a].add(b)
    return res


def get_break_map(rule_list: list[tuple[int, int]]) -> dict[int, set[int]]:
    res = defaultdict(set)
    for a, b in rule_list:
        res[b].add(a)
    return res


def has_cycle(rule_map: dict[int, list[int]]) -> bool:
    """make sure the rule_map graph has no cycle"""
    visited = set()
    recursion_stack = set()

    def dfs(node):
        visited.add(node)
        recursion_stack.add(node)

        for neighbor in rule_map.get(node, []):
            if neighbor in recursion_stack:
                return True
            if neighbor not in visited:
                if dfs(neighbor):
                    return True

        recursion_stack.remove(node)
        return False

    for node in rule_map:
        if node not in visited:
            if dfs(node):
                return True

    return False


def verify_rules(line, break_map):
    for idx, elt in enumerate(line[:-1]):
        if forbidden := break_map.get(elt):
            if forbidden & set(line[idx + 1 :]):
                return False
    return True


def get_middle(line):
    return line[len(line) // 2]


def custom_compare(a, b, rule_map):
    if b in rule_map.get(a, set()):
        return -1
    if a in rule_map.get(b, set()):
        return 1
    return -1


def custom_sort(line, rule_map):
    return sorted(line, key=cmp_to_key(partial(custom_compare, rule_map=rule_map)))


def resolve1():
    ordering_rules, instr_list = parse_input("input.txt")
    break_map = get_break_map(ordering_rules)
    return sum(get_middle(line) for line in instr_list if verify_rules(line, break_map))


def resolve2():
    ordering_rules, lines = parse_input("input.txt")
    rule_map = get_rule_map(ordering_rules)

    return sum(
        get_middle(ordered_line)
        for line in lines
        if (ordered_line := custom_sort(line, rule_map)) != line
    )


if __name__ == "__main__":
    print(resolve1())
    print(resolve2())
