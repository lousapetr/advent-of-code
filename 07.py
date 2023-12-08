"""
--- Day 7: Camel Cards ---

https://adventofcode.com/2023/day/7
"""

from __future__ import annotations

import re
from functools import cached_property, total_ordering

from wrapper import Wrapper


@total_ordering
class Card:
    _value_dict = {face: value for value, face in enumerate("23456789TJQKA")}

    def __init__(self, face: str) -> None:
        self.face = face
        self.value = self._value_dict[self.face]

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
    def __init__(self, cards: str, bid: int) -> None:
        self.cards_str = cards
        self.cards_sorted_str = "".join(sorted(cards))
        self.cards = [Card(c) for c in cards]
        self.bid = bid

    @cached_property
    def type_rank(self) -> int:
        """
        Evaluate the type of hand, assign numerical value to it.

        Returns:
            int: the higher the rank, the higher type = "high card" -> 0
        """
        patterns = [
            r"(.)\1{4}",  # five of a kind
            r"(.)\1{3}",  # four of a kind
            r"(.)\1{2}(.)\2|(.)\3(.)\4{2}",  # full house (AAABB or AABBB)
            r"(.)\1{2}",  # three of a kind
            r"(.)\1.*(.)\2",  # two pair
            r"(.)\1",  # one pair
            r".",  # high card
        ]
        for i, pattern in enumerate(patterns):
            rank = len(patterns) - i
            if re.search(pattern, self.cards_sorted_str):
                return rank
        raise ValueError(f"Rank of {self.cards_sorted_str} cannot be determined")

    def __repr__(self) -> str:
        return f"Hand({self.cards_str}, {self.bid})"

    def __eq__(self, other: Hand) -> bool:
        return self.cards_str == other.cards_str

    def __lt__(self, other: Hand) -> bool:
        if self.type_rank != other.type_rank:
            return self.type_rank < other.type_rank
        else:
            return self.cards < other.cards


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom

    def parse_custom(self, path) -> list[Hand]:
        hands = []
        with open(path) as f:
            for line in f:
                line_split = line.strip().split()
                hand = Hand(line_split[0], int(line_split[1]))
                hands.append(hand)
        return hands

    def task_1(self):
        sorted_hands = sorted(self.input)
        return sum((rank + 1) * hand.bid for rank, hand in enumerate(sorted_hands))

    def task_2(self):
        return NotImplemented


part = 1
solve_example = True
solve_example = False
example_solutions = [6440, None]

solver = Solver(day=7, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
