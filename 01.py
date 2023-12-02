from typing import Dict, List, Set, Tuple  # noqa: F401

from wrapper import Wrapper

# --- Day 1: Trebuchet?! ---
# https://adventofcode.com/2023/day/1

DAY_NUMBER = 1


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_to_list

    def task_1(self):
        digits = ["".join(filter(lambda x: x.isdigit(), line)) for line in self.input]
        numbers = [int(d[0] + d[-1]) for d in digits]
        return sum(numbers)

    def task_2(self):
        return NotImplemented


part = 1

solve_example = True
solve_example = False
example_solutions = [142, None]

solver = Solver(day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
