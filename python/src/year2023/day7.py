from itertools import product
from time import time
from typing import Any, ClassVar


class Hand:
    card_values: ClassVar[dict[str, int]] = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 11,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }

    def __init__(self, cards: str, bid: str) -> None:
        self.bid = bid
        self.cards = cards

    def __repr__(self) -> str:
        return f"Hand({self.cards}, {self.bid})"

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Hand):
            msg = "Comparison between Card and not-Card is not supported."
            raise NotImplementedError(msg)

        if self.value(self.cards) != self.value(other.cards):
            return self.value(self.cards) < self.value(other.cards)

        for my_card, other_card in zip(self.cards, other.cards, strict=False):
            if self.card_values[my_card] != self.card_values[other_card]:
                return self.card_values[my_card] < self.card_values[other_card]

        msg = f"Could not compare cards: {self.cards} and {other.cards}."
        raise RuntimeError(msg)

    @staticmethod
    def value(cards: str) -> int:  # noqa: C901, PLR0911
        if not cards:
            return 0

        count_cards: dict[str, int] = {}
        for card in cards:
            if card not in count_cards:
                count_cards[card] = 1
                continue
            count_cards[card] += 1

        # five of a kind
        if len(count_cards) == 1:
            return 7
        # four of a kind
        if len(count_cards) == 2 and max(count_cards.values()) == 4:
            return 6
        # full house
        if len(count_cards) == 2 and max(count_cards.values()) == 3:
            return 5
        # three of a kind
        if len(count_cards) == 3 and max(count_cards.values()) == 3:
            return 4
        # two pairs
        if len(count_cards) == 3 and max(count_cards.values()) == 2:
            return 3
        # one pair
        if len(count_cards) == 4:
            return 2
        # high card
        if len(count_cards) == 5:
            return 1

        msg = f"Could not calculate value of a hand: {cards}"
        raise RuntimeError(msg)


class JokerHand(Hand):
    card_values: ClassVar[dict[str, int]] = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 1,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }

    def value(self, cards: str) -> int:
        best_hand = ""
        no_joker_hand = cards.replace("J", "")

        if cards == no_joker_hand:
            return super().value(cards)

        available_cards = [key for key in self.card_values if key != "J"]

        for added_cards in product(available_cards, repeat=5 - len(no_joker_hand)):
            hand = no_joker_hand + "".join(added_cards)
            if super().value(hand) > super().value(best_hand):
                best_hand = hand

        return super().value(best_hand)


def day7() -> None:
    with open("inputs/2023/day7.txt", encoding="utf-8") as file:
        lines = file.readlines()

    # part 1
    hands = [Hand(*line.strip().split()) for line in lines]
    hands.sort()
    print(sum(i * int(hand.bid) for i, hand in enumerate(hands, start=1)))

    # part 2
    joker_hands = [JokerHand(hand.cards, hand.bid) for hand in hands]
    joker_hands.sort()
    print(sum(i * int(hand.bid) for i, hand in enumerate(joker_hands, start=1)))


if __name__ == "__main__":
    start = time()
    day7()
    print(f"Execution time: {round(time() - start)} seconds.")
