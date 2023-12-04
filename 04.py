import re

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

    def task_1(self):
        wins = []
        for card in self.input:
            card_id, winning, my_nums = card
            wins.append(winning & my_nums)
            # print(card_id, winning & my_nums)
        points = 0
        for win in wins:
            if win:
                points += 2 ** (len(win) - 1)
        return points

    def task_2(self):
        return NotImplemented


part = 1
solve_example = True
solve_example = False
example_solutions = [13, None]

solver = Solver(day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
