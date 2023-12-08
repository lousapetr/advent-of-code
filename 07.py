"""
--- Day 7: Camel Cards ---

https://adventofcode.com/2023/day/7
"""

from __future__ import annotations

import re
from functools import cached_property, total_ordering
from pprint import pprint
from typing import Type

from wrapper import Wrapper


@total_ordering
class Card:
    faces = "23456789TJQKA"

    def __init__(self, face: str) -> None:
        self.face = face
        value_dict = {face: value for value, face in enumerate(self.faces)}
        self.value = value_dict[self.face]

    def __repr__(self) -> str:
        return f"Card({self.face})"

    def __str__(self) -> str:
        return self.face

    def __eq__(self, other: Card) -> bool:
        return self.value == other.value

    def __lt__(self, other: Card) -> bool:
        return self.value < other.value


@total_ordering
class Hand:
    patterns = [
        r"(.)\1{4}",  # five of a kind
        r"(.)\1{3}",  # four of a kind
        r"(.)\1{2}(.)\2|(.)\3(.)\4{2}",  # full house (AAABB or AABBB)
        r"(.)\1{2}",  # three of a kind
        r"(.)\1.*(.)\2",  # two pair
        r"(.)\1",  # one pair
        r".",  # high card
    ]

    def __init__(self, cards: str, bid: int) -> None:
        self.cards_str = cards
        self.cards_sorted_str = "".join(sorted(cards))
        self.cards = [Card(c) for c in cards]
        self.bid = bid

    def _matched_pattern(self, cards_sorted: str) -> int:
        """
        Evaluate the type of hand, assign numerical value to it.

        Returns:
            int: the higher the rank, the higher type = "high card" -> 0
        """
        for i, pattern in enumerate(self.patterns):
            rank = len(self.patterns) - i
            if re.search(pattern, cards_sorted):
                return rank
        raise ValueError(f"Rank of {cards_sorted} cannot be determined")

    @cached_property
    def type_rank(self) -> int:
        """
        Evaluate the type of hand, assign numerical value to it.

        Returns:
            int: the higher the rank, the higher type = "high card" -> 0
        """
        return self._matched_pattern(self.cards_sorted_str)

    def __repr__(self) -> str:
        return f"""Hand("{self.cards_str}", {self.bid})"""

    def __eq__(self, other: Hand) -> bool:
        return self.cards_str == other.cards_str

    def __lt__(self, other: Hand) -> bool:
        if self.type_rank != other.type_rank:
            return self.type_rank < other.type_rank
        else:
            return self.cards < other.cards


class Card_2(Card):
    faces = "J23456789TQKA"

    def __init__(self, face: str) -> None:
        super().__init__(face)


class Hand_2(Hand):
    patterns = [
        r"(.)(\1|J){4}",  # five of a kind
        r"(.)(.*(\1|J)){3}",  # four of a kind
        r"(?P<a1>.)((?P=a1)|J){2}(?P<a2>.)(?P=a2)"  # full house AAABB
        r"|(?P<b1>.)(?P=b1)(?P<b2>.)((?P=b2)|J){2}",  # full house AABBB
        r"(.)(.*(\1|J)){2}",  # three of a kind
        r"(?P<a>.)(.*((?P=a)|J)).*(?P<b>.)(.*((?P=b)|J))",  # two pair
        r"(.).*(\1|J)",  # one pair
        r".",  # high card
    ]

    def __init__(self, cards: str, bid: int) -> None:
        super().__init__(cards, bid)
        self.cards = [Card_2(c) for c in cards]
        self.cards_sorted_str = self.cards_sorted_str.replace("J", "") + "J" * cards.count("J")

    def __repr__(self) -> str:
        return f"""Hand_2("{self.cards_str}", {self.bid})"""


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom

    def parse_custom(self, path) -> list[tuple[str, int]]:
        hands = []
        with open(path) as f:
            for line in f:
                line_split = line.strip().split()
                hand = (line_split[0], int(line_split[1]))
                hands.append(hand)
        return hands

    def task(self, hand_class: Type[Hand]):
        hands = [hand_class(*h) for h in self.input]
        sorted_hands = sorted(hands)
        pprint([[h, h.type_rank] for h in sorted_hands])
        return sum((rank + 1) * hand.bid for rank, hand in enumerate(sorted_hands))

    def task_1(self):
        return self.task(Hand)

    def task_2(self):
        return self.task(Hand_2)


part = 2
solve_example = True
solve_example = False
example_solutions = [(6440, 6592), (5905, 6839)]

solver = Solver(day=7, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
# solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
