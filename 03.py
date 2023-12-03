import re
from typing import Match

from wrapper import Wrapper

# --- Day 3: Gear Ratios ---
# https://adventofcode.com/2023/day/3

DAY_NUMBER = 3

MatchType = tuple[int, Match[str]]


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

    def find_items(self, plan: list[str], pattern: str) -> list[MatchType]:
        matches = []
        for n, line in enumerate(plan):
            line_matches = re.finditer(pattern, line)
            matches += [(n, m) for m in line_matches]
        return matches

    def neighborhood(self, match: MatchType, plan: list[str]) -> str:
        row = match[0]
        span = match[1].span()
        top = plan[row - 1][span[0] - 1 : span[1] + 1]
        bottom = plan[row + 1][span[0] - 1 : span[1] + 1]
        left = plan[row][span[0] - 1]
        right = plan[row][span[1]]
        return top + bottom + left + right

    def task_1(self):
        bordered = self.add_borders()
        matches = self.find_items(bordered, r"\d+")
        engine_parts = []
        for m in matches:
            if re.findall(r"[^0-9.]", n := self.neighborhood(m, bordered)):
                engine_parts.append(int(m[1].group()))
            print(m, n)
        print(engine_parts)
        return sum(engine_parts)

    def gear_numbers(self, gears: list[MatchType], numbers: list[MatchType]) -> list[tuple[int, int]]:
        gear_ratios = []
        for gear in gears:
            gear_row, gear_col = gear[0], gear[1].start()
            attached_numbers = []
            for n_row, n_match in numbers:
                if gear_row - 1 <= n_row <= gear_row + 1:
                    if (gear_col <= n_match.end()) and (gear_col + 1 >= n_match.start()):
                        # print(n_match)
                        attached_numbers.append(int(n_match.group()))
            # print(gear, attached_numbers)
            if len(attached_numbers) == 2:
                gear_ratios.append(attached_numbers)
        return gear_ratios

    def task_2(self):
        bordered = self.add_borders()
        # print(self.array_to_string(bordered, format="s"))
        numbers = self.find_items(bordered, r"\d+")
        gears = self.find_items(bordered, r"\*")
        gear_ratios = self.gear_numbers(gears, numbers)
        # print(gear_ratios)
        return sum([gr[0] * gr[1] for gr in gear_ratios])


part = 2
solve_example = True
solve_example = False
example_solutions = [4361, 467835]

solver = Solver(day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
