import re
from collections import Counter

from wrapper import Wrapper

# --- Day 4: Scratchcards ---
# https://adventofcode.com/2023/day/4

DAY_NUMBER = 4


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom

    def parse_custom(self, path) -> list[tuple[int, set[int], set[int]]]:
        cards = []
        with open(path) as f:
            for line in f:
                if not line.strip():
                    continue
                card_id = int(re.search(r"Card *(\d+)", line).group(1))
                winning_numbers_str = re.search(r":(.*)\|", line).group(1)
                winning_numbers = {int(n) for n in re.findall(r"\d+", winning_numbers_str)}
                my_numbers_str = re.search(r"\|(.*)$", line).group(1)
                my_numbers = {int(n) for n in re.findall(r"\d+", my_numbers_str)}
                cards.append((card_id, winning_numbers, my_numbers))
        return cards

    def number_of_wins(self) -> dict[int, int]:
        wins = {}
        for card in self.input:
            card_id, winning, my_nums = card
            matches = winning & my_nums
            wins[card_id] = len(matches)
        return wins

    def task_1(self):
        points = 0
        for matches in self.number_of_wins().values():
            if matches:
                points += 2 ** (matches - 1)
        return points

    def task_2(self):
        cards = Counter()
        wins = self.number_of_wins()
        # print(sorted(cards.items()))
        for card_id in sorted(wins.keys()):
            cards[card_id] += 1
            cards_won = wins[card_id]
            new_cards = {(card_id + 1 + i): cards[card_id] for i in range(cards_won)}
            cards.update(new_cards)
            # print(sorted(cards.items()))
        return sum(cards.values())


part = 2
solve_example = True
solve_example = False
example_solutions = [13, 30]

solver = Solver(day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
