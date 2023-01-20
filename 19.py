from typing import Dict, List, Set, Tuple  # noqa: F401

from wrapper import Wrapper

# --- Day 19: Not Enough Minerals ---
# https://adventofcode.com/2022/day/19

DAY_NUMBER = 19


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom

    def parse_custom(self, path):
        with open(path) as f:
            for line in f:
                pass

    def task_1(self):
        return NotImplemented

    def task_2(self):
        return NotImplemented


part = 1
solve_example = True
# solve_example = False
example_solutions = [None, None]

solver = Solver(day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
