from typing import Dict, List, Set, Tuple  # noqa: F401

from wrapper import Wrapper

# --- Day 23: Unstable Diffusion ---
# https://adventofcode.com/2022/day/23

DAY_NUMBER = 23


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom

    def parse_custom(self, path) -> Set[Tuple[int, int]]:
        lines = self.parse_to_list(path, comment="-")
        elf_positions = set()
        for i, line in enumerate(lines):
            for j, char in enumerate(line):
                if char == "#":
                    elf_positions.add((i, j))  # row, col
        return elf_positions

    def task_1(self):
        return NotImplemented

    def task_2(self):
        return NotImplemented


part = 1
solve_example = True
# solve_example = False
example_solutions = [110, None]

solver = Solver(day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
