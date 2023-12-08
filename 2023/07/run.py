from collections import Counter
from dataclasses import dataclass
from pathlib import Path

# 6 - five of a kind
# 5 - four of a kind
# 4 - full house (3+2)
# 3 - three of a kind
# 2 - two pairs
# 1 - one pair
# 0 - high card


class InvalidCase(Exception):
    ...


class HandType:
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIRS = 2
    ONE_PAIR = 1
    HIGH_CARD = 0


@dataclass
class Hand:
    cards: str
    count_joker: bool = False

    def __lt__(self, other):
        return comp_cards(self.cards, other.cards, self.count_joker)


def sym_to_value(sym: str, count_joker=False) -> int:
    val = {
        "2": 0,
        "3": 1,
        "4": 2,
        "5": 3,
        "6": 4,
        "7": 5,
        "8": 6,
        "9": 7,
        "T": 8,
        "J": 9,
        "Q": 10,
        "K": 11,
        "A": 12,
    }[sym] + 1
    if count_joker and sym == "J":
        return 0
    return val


def hand_value(cards):
    counter = Counter(cards)
    values = sorted(list(counter.values()), reverse=True)
    if values[0] == 5:
        return 6
    elif values[0] == 4:
        return 5
    elif values == [3, 2]:
        return 4
    elif values[0] == 3:
        return 3
    elif values[:2] == [2, 2]:
        return 2
    elif values[0] == 2:
        return 1
    elif len(values) == 5:
        return 0
    raise ValueError(f"Invalid hand: {cards}")


def hand_value_joker(cards):
    counter = Counter(cards)
    j_count = counter.get("J", 0)
    values = sorted(list(counter.values()), reverse=True)

    # FIVE_OF_A_KIND
    if values[0] == 5:
        return HandType.FIVE_OF_A_KIND

    # FOUR_OF_A_KIND
    elif values[0] == 4:
        if j_count in [1, 4]:
            return HandType.FIVE_OF_A_KIND
        elif j_count != 0:
            raise InvalidCase(cards)
        return HandType.FOUR_OF_A_KIND

    # FULL_HOUSE
    elif values == [3, 2]:
        if j_count in [2, 3]:
            return HandType.FIVE_OF_A_KIND
        elif j_count != 0:
            raise InvalidCase(cards)
        return HandType.FULL_HOUSE

    # THREE_OF_A_KIND
    elif values[0] == 3:
        if j_count in [1, 3]:
            return HandType.FOUR_OF_A_KIND
        elif j_count != 0:
            raise InvalidCase(cards)
        return HandType.THREE_OF_A_KIND

    # TWO_PAIRS
    elif values[:2] == [2, 2]:
        if j_count == 1:
            return HandType.FULL_HOUSE
        elif j_count == 2:
            return HandType.FOUR_OF_A_KIND
        elif j_count != 0:
            raise InvalidCase(cards)
        return HandType.TWO_PAIRS

    # ONE_PAIR
    elif values[0] == 2:
        if j_count in [1, 2]:
            return HandType.THREE_OF_A_KIND
        elif j_count != 0:
            raise InvalidCase(cards)
        return HandType.ONE_PAIR

    # HIGH_CARD
    elif len(values) == 5:
        if j_count == 1:
            return HandType.ONE_PAIR
        elif j_count != 0:
            raise InvalidCase(cards)
        return HandType.HIGH_CARD
    raise InvalidCase(cards)


def comp_cards(hand1: str, hand2: str, count_joker: bool = False) -> bool:
    _hand_value = hand_value_joker if count_joker else hand_value

    val1, val2 = _hand_value(hand1), _hand_value(hand2)
    if val1 != val2:
        return val1 < val2

    for idx in range(5):
        c_val1, c_val2 = sym_to_value(hand1[idx], count_joker), sym_to_value(
            hand2[idx], count_joker
        )
        if c_val1 != c_val2:
            return c_val1 < c_val2

    raise ValueError(f"Identical hands: {hand1}")


def parse_input(path: str):
    p = Path(__file__).resolve().parent / path

    return [l.split() for l in p.read_text().splitlines()]


def resolve1():
    lines = parse_input("input.txt")
    lines.sort(key=lambda l: Hand(l[0]))
    return sum((idx + 1) * int(value) for idx, (_, value) in enumerate(lines))


def resolve2():
    lines = parse_input("input.txt")
    lines.sort(key=lambda l: Hand(l[0], True))
    return sum((idx + 1) * int(value) for idx, (_, value) in enumerate(lines))


if __name__ == "__main__":
    print(
        Hand("JKKK2", True) < Hand("QQQQ2", True),
        sym_to_value("J", True),
        sym_to_value("Q", True),
    )
    print(resolve1())
    print(resolve2())
