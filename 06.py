from wrapper import Wrapper
from typing import List, Tuple, Set, Dict  # noqa: F401

# https://adventofcode.com/2022/day/6

DAY_NUMBER = 6


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_to_list
        self.input = super().load_input()[0]

    def task_1(self):
        for i in range(4, len(self.input)):
            substring = self.input[i - 4 : i]
            if len(substring) == len(set(substring)):
                return i

    def task_2(self):
        return NotImplemented


part = 1
solve_example = True
solve_example = False
example_solutions = [7, None]

solver = Solver(
    day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions
)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
