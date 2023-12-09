"""
--- Day 5: If You Give A Seed A Fertilizer ---

https://adventofcode.com/2023/day/5
"""

import re
from collections import OrderedDict
from pprint import pprint

from wrapper import Wrapper


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom

    def parse_custom(self, path) -> dict[str, list[tuple[int, int, int]]]:
        data = OrderedDict()
        with open(path) as f:
            blocks = f.read().split("\n\n")
        data["seeds"] = [int(n) for n in re.findall(r"\d+", blocks[0])]
        for block in blocks[1:]:
            lines = block.splitlines()
            name = lines[0].split()[0]
            rules_orig = [[int(n) for n in re.findall(r"\d+", line)] for line in lines[1:]]
            data[name] = []
            for rule in rules_orig:
                start_target, start_source, length = rule
                end_source = start_source + length - 1
                modifier = start_target - start_source
                data[name].append((start_source, end_source, modifier))
            data[name] = sorted(data[name])
        return data

    @staticmethod
    def find_next(number: int, rules: list[list[int]]) -> int:
        for rule in rules:
            start_source, end_source, modifier = rule
            if start_source <= number <= end_source:
                return number + modifier
        return number  # don't change if not covered by any rule

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

    def find_new_ranges(self, old_start: int, old_end: int, rules_name: str) -> list[tuple[int, int]]:
        rules = self.input[rules_name]
        for rule in rules:
            start_source, end_source, modifier = rule
            # find appropriate rule
            if start_source <= old_start <= end_source:
                new_start = old_start + modifier
                # original range fits into a single rule
                if old_end <= end_source:
                    return [(new_start, old_end + modifier)]
                else:
                    return [(new_start, end_source + modifier)] + self.find_new_ranges(
                        end_source + 1, old_end, rules_name
                    )
        # no rule was found
        else:
            larger_rule_starts = [r[0] for r in rules if r[0] > old_start]
            if larger_rule_starts:
                next_rule_start = min(larger_rule_starts)
                if old_end >= next_rule_start:
                    return [(old_start, next_rule_start - 1)] + self.find_new_ranges(
                        next_rule_start, old_end, rules_name
                    )
            # either old start is above all rules, or full range fits between rules
            return [(old_start, old_end)]

    def task_2(self):
        seeds = self.input.pop("seeds")
        old_ranges = sorted([(seeds[i - 1], seeds[i - 1] + seeds[i] - 1) for i in range(1, len(seeds), 2)])
        print("Seeds:", old_ranges)
        for name in self.input:
            new_ranges = []
            for old_range in old_ranges:
                new_ranges += self.find_new_ranges(*old_range, name)
            old_ranges = sorted(new_ranges).copy()
            print(name)
            pprint(old_ranges)
        return old_ranges[0][0]


part = 2
solve_example = True
solve_example = False
example_solutions = [35, 46]

solver = Solver(day=5, example=solve_example, example_solutions=example_solutions)  # noqa: F821
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
