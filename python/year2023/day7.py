from itertools import combinations
from time import time
from typing import Any


class Hand:
    card_values = {"A": 14, "K": 13, "Q": 12, "J": 11, "T": 10, "9": 9, "8": 8, "7": 7, "6": 6,
                   "5": 5, "4": 4, "3": 3, "2": 2}

    def __init__(self, cards: str, bid: str) -> None:
        self.bid = bid
        self.cards = cards

    def __lt__(self, other: Any):
        if not isinstance(other, Hand):
            raise NotImplementedError("Comparison between Card and not-Card is not supported.")

        if self.value(self.cards) != self.value(other.cards):
            return self.value(self.cards) < self.value(other.cards)

        for my_card, other_card in zip(self.cards, other.cards):
            if self.card_values[my_card] != self.card_values[other_card]:
                return self.card_values[my_card] < self.card_values[other_card]

        raise RuntimeError(f"Could not compare cards: {self.cards} and {other.cards}.")

    def value(self, cards: str) -> int:
        count_cards: dict[str, int] = {}
        for card in cards:
            if card not in count_cards:
                count_cards[card] = 1
                continue
            count_cards[card] += 1

        # five of a kind
        if len(count_cards) == 1:
            return 6
        # four of a kind
        if len(count_cards) == 2 and max(count_cards.values()) == 4:
            return 5
        # full house
        if len(count_cards) == 2 and max(count_cards.values()) == 3:
            return 4
        # three of a kind
        if len(count_cards) == 3 and max(count_cards.values()) == 3:
            return 3
        # two pairs
        if len(count_cards) == 3 and max(count_cards.values()) == 2:
            return 2
        # one pair
        if len(count_cards) == 4:
            return 1
        # high card
        if len(count_cards) == 5:
            return 0

        raise RuntimeError(f"Could not calculate value of a hand: {cards}")


class JokerHand(Hand):
    card_values = {"A": 14, "K": 13, "Q": 12, "J": 1, "T": 10, "9": 9, "8": 8, "7": 7, "6": 6,
                   "5": 5, "4": 4, "3": 3, "2": 2}

    def value(self, cards: str) -> int:
        best_hand = cards
        no_joker_hand = cards.replace("J", "")

        if cards == no_joker_hand:
            return super().value(cards)

        available_cards = [key for key in self.card_values.keys() if key != "J"]

        for added_cards in combinations(available_cards, 5 - len(no_joker_hand)):
            hand = no_joker_hand.join(added_cards)
            if super().value(hand) > super().value(best_hand):
                best_hand = hand
        
        return super().value(best_hand)


def day7() -> None:
    with open("inputs/2023/day7.txt", "r") as file:
        lines = file.readlines()

    # part 1
    hands = [Hand(*line.strip().split()) for line in lines]
    hands.sort()
    print(sum(i * int(hand.bid) for i, hand in enumerate(hands, start=1)))

    # part 2
    # joker_hands = [JokerHand(hand.cards, hand.bid) for hand in hands]
    # joker_hands.sort()
    # print(sum(i * int(hand.bid) for i, hand in enumerate(joker_hands, start=1)))


if __name__ == "__main__":
    start = time()
    day7()
    print(f"Execution time: {round((time() - start))} seconds.")
