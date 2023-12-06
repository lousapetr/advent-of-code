"""
--- Day 6: Wait For It ---

https://adventofcode.com/2023/day/6
"""

import math
import re

from wrapper import Wrapper


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom

    def parse_custom(self, path) -> tuple[list[int], list[int]]:
        with open(path) as f:
            times_str = f.readline()
            distance_str = f.readline()
        times = [int(n) for n in re.findall(r"\d+", times_str)]
        distances = [int(n) for n in re.findall(r"\d+", distance_str)]
        return times, distances

    def task_1(self):
        winning_ways = []
        for time, dist in zip(*self.input):
            # print(f"{time=} {dist=}")
            # the question is equivalent to
            # how many integers solve equation `x*(time-x) - dist > 0`?
            # equation is equivalent to `x**2 - time*x + dist < 0`
            dist += 1e-6  # avoid the roots being exact integers
            discriminant = time**2 - 4 * dist
            # print(f"{discriminant=}")
            # (7 +- 3.5) / 2
            root_low = (time - discriminant**0.5) / 2
            root_high = (time + discriminant**0.5) / 2
            wins = math.floor(root_high) - math.ceil(root_low) + 1
            winning_ways.append(wins)
        print(f"{winning_ways=}")
        return math.prod(winning_ways)

    def task_2(self):
        return NotImplemented


part = 1
solve_example = True
solve_example = False
example_solutions = [288, None]

solver = Solver(day=6, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
