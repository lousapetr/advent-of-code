"""
--- Day 5: If You Give A Seed A Fertilizer ---

https://adventofcode.com/2023/day/5
"""

import re

from wrapper import Wrapper


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom

    def parse_custom(self, path) -> dict[str, list[list[int]]]:
        data = {}
        with open(path) as f:
            blocks = f.read().split("\n\n")
        data["seeds"] = [int(n) for n in re.findall(r"\d+", blocks[0])]
        for block in blocks[1:]:
            lines = block.splitlines()
            name = lines[0].split()[0]
            rules = [[int(n) for n in re.findall(r"\d+", line)] for line in lines[1:]]
            data[name] = rules
        return data

    @staticmethod
    def find_next(number: int, rules: list[list[int]]) -> int:
        result = number
        for rule in rules:
            start_target, start_source, length = rule
            if start_source <= number < start_source + length:
                result = number + start_target - start_source
        return result

    def task_1(self):
        locations = []
        seeds = self.input.pop("seeds")
        for seed in seeds:
            value = seed
            for name, rules in self.input.items():
                # print(f"{value=}")
                # print(f"{name=}")
                value = self.find_next(value, rules)
            # print(f"{value=}")
            locations.append(value)
            # print()
        return min(locations)

    def task_2(self):
        return NotImplemented


part = 1
solve_example = True
solve_example = False
example_solutions = [35, None]

solver = Solver(day=5, example=solve_example, example_solutions=example_solutions)  # noqa: F821
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
