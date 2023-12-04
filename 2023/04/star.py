from dataclasses import dataclass


@dataclass
class Card:
    winning_numbers: list[int]
    numbers: list[str]

    @staticmethod
    def from_line(line: str) -> "Card":
        tmp = line.split(": ", 1)[1].split(" | ")
        card = [[int(numb) for numb in str_numb.split()] for str_numb in tmp]
        return Card(winning_numbers=card[0], numbers=card[1])

    @property
    def matches(self) -> list[int]:
        return [value for value in self.winning_numbers if value in self.numbers]

    @property
    def value(self):
        return pow(2, match_count - 1) if (match_count := len(self.matches)) else 0


def resolve2():
    with open("2023/04/input.txt") as f:
        input_str = f.read()

    cards = [Card.from_line(line) for line in input_str.splitlines()]
    card_counts = get_card_counts(cards)
    return sum(card_counts.values())


def get_card_counts(cards: list[Card]) -> dict[int, int]:
    card_counts = {card_idx: 1 for card_idx, card in enumerate(cards)}

    for card_idx in card_counts:
        card = cards[card_idx]
        for match_idx, _ in enumerate(card.matches):
            for _ in range(card_counts[card_idx]):
                try:
                    card_counts[card_idx + match_idx + 1] += 1
                except KeyError:
                    pass
    return card_counts


def resolve1():
    with open("2023/04/input.txt") as f:
        input_str = f.read()

    cards = [Card.from_line(line) for line in input_str.splitlines()]
    return sum(card.value for card in cards)


if __name__ == "__main__":
    print(resolve1())
    print(resolve2())
