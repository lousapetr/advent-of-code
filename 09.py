"""
--- Day 9: Mirage Maintenance ---

https://adventofcode.com/2023/day/9
"""

from pprint import pprint  # noqa: F401

from wrapper import Wrapper


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_to_list
        self.parser_kwargs = {"astype": lambda line: [int(x) for x in line.split()]}

    def get_diffs(self, array: list[int]) -> list[int]:
        return [array[i] - array[i - 1] for i in range(1, len(array))]

    def alternating_sum(self, array: list[int]) -> int:
        """
        Calculate alternating sum for backward filling.

        If first values of differences are [10, 3, 0, 2, 0], the backfill should
        be calculated as `10 - (3 - (0 - (2 - 0)))` which corresponds
        to `10 - 3 + 0 - 2 + 0`.
        """
        elements_even = array[::2]
        elements_odd = array[1::2]
        return sum(elements_even) - sum(elements_odd)

    def task(self, task_number: int) -> int:
        futures = []
        backwards = []
        for history in self.input:
            last_values = [history[-1]]
            first_values = [history[0]]
            while any(history):
                history = self.get_diffs(history)
                last_values.append(history[-1])
                first_values.append(history[0])
            backwards.append(self.alternating_sum(first_values))
            futures.append(sum(last_values))
        if task_number == 1:
            return sum(futures)
        else:
            return sum(backwards)

    def task_1(self):
        return self.task(1)

    def task_2(self):
        return self.task(2)


part = 2
solve_example = True
solve_example = False
example_solutions = [114, 2]

solver = Solver(day=9, example=solve_example, example_solutions=example_solutions)
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
