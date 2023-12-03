import re
from typing import Match

from wrapper import Wrapper

# --- Day 3: Gear Ratios ---
# https://adventofcode.com/2023/day/3

DAY_NUMBER = 3


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_to_list

    def add_borders(self) -> list[str]:
        bordered = self.input.copy()
        empty_line = "." * len(bordered[0])
        bordered = [empty_line] + bordered + [empty_line]
        bordered = [f".{line}." for line in bordered]
        return bordered

    def find_numbers(self, plan: list[str]) -> list[tuple[int, Match[str]]]:
        matches = []
        for n, line in enumerate(plan):
            line_matches = re.finditer(r"\d+", line)
            matches += [(n, m) for m in line_matches]
        return matches

    def neighborhood(self, match: tuple[int, Match[str]], plan: list[str]) -> str:
        row = match[0]
        span = match[1].span()
        top = plan[row - 1][span[0] - 1 : span[1] + 1]
        bottom = plan[row + 1][span[0] - 1 : span[1] + 1]
        left = plan[row][span[0] - 1]
        right = plan[row][span[1]]
        return top + bottom + left + right

    def task_1(self):
        bordered = self.add_borders()
        # print("\n".join(bordered))
        matches = self.find_numbers(bordered)
        engine_parts = []
        for m in matches:
            if re.findall(r"[^0-9.]", n := self.neighborhood(m, bordered)):
                engine_parts.append(int(m[1].group()))
            print(m, n)
        print(engine_parts)
        return sum(engine_parts)

    def task_2(self):
        return NotImplemented


part = 1
solve_example = True
solve_example = False
example_solutions = [4361, None]

solver = Solver(day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
