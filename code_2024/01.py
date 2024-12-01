"""
--- Day 1: Historian Hysteria ---

https://adventofcode.com/2024/day/1
"""

from collections import Counter

import pandas as pd

from advent_of_code.wrapper import Wrapper


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.input: pd.DataFrame
        self.parser = self.parse_to_pandas_df

    def task_1(self) -> int:
        list_left = self.input.iloc[:, 0]
        list_right = self.input.iloc[:, 1]
        diff = list_right.sort_values() - list_left.sort_values().values
        return sum(abs(diff))

    def task_2(self):
        list_left = self.input.iloc[:, 0]
        list_right = self.input.iloc[:, 1]
        counter_right = Counter(list_right)
        return sum(num * counter_right[num] for num in list_left)


part = 2
solve_example = True
solve_example = False
example_solutions = [11, 31]

solver = Solver(year=2024, day=1)
# solve always all examples, but only one final task
if solve_example:
    for p in range(1, part + 1):
        solver.solve_examples(p, example_solutions[p - 1])
else:
    solver.solve_task(part, verbose=False)
    # solver.submit_answer(part)
