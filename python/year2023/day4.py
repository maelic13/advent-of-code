from time import time_ns


class Card:
    def __init__(self, card_id: int, winning_numbers: list[int], my_numbers: list[int]) -> None:
        self.card_id = card_id
        self.my_numbers = my_numbers
        self.winning_numbers = winning_numbers

    def __repr__(self) -> str:
        return f"Card {self.card_id}"

    @property
    def my_winning_numbers(self) -> set[int]:
        return set(self.my_numbers).intersection(self.winning_numbers)

    @property
    def num_winning_numbers(self) -> int:
        return len(self.my_winning_numbers)

    @property
    def worth(self) -> int:
        num_winning_numbers = self.num_winning_numbers
        if num_winning_numbers == 0:
            return 0
        return 2 ** (num_winning_numbers - 1)


def day4() -> None:
    with open("inputs/2023/day4.txt", "r") as file:
        lines = file.readlines()

    cards: list[Card] = []
    for line in lines:
        card_name, numbers = line.strip().split(": ")
        card_id = int(card_name.split()[1])

        winning_numbers, my_numbers = numbers.split(" | ")
        cards.append(Card(card_id, list(map(int, winning_numbers.split())),
                          list(map(int, my_numbers.split()))))

    # part 1
    print(sum(card.worth for card in cards))

    # part 2
    card_instances: dict[Card, int] = {card: 1 for card in cards}
    for card_num, card in enumerate(cards):
        for x in range(card_num + 1, card_num + card.num_winning_numbers + 1):
            card_instances[cards[x]] += 1 * card_instances[card]

    print(sum(card_instances.values()))


if __name__ == "__main__":
    start = time_ns()
    day4()
    print(f"Execution time: {round((time_ns() - start) // 1000)} microseconds.")
