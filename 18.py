from wrapper import Wrapper
from typing import List, Tuple, Set, Dict  # noqa: F401

# https://adventofcode.com/2022/day/18

DAY_NUMBER = 18


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
example_solutions = [64, None]

solver = Solver(day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
