"""
--- Day 11: Cosmic Expansion ---

https://adventofcode.com/2023/day/11
"""
from __future__ import annotations

from functools import partial
from pprint import pprint  # noqa: F401

from wrapper import Wrapper


class Galaxy:
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

    def __sub__(self, other: Galaxy) -> int:
        """
        Calculate Manhattan distance
        """
        vertical = self.row - other.row
        horizontal = self.col - other.col
        return abs(vertical) + abs(horizontal)

    def __repr__(self) -> str:
        return f"Galaxy(row={self.row}, col={self.col})"


class Universe:
    def __init__(self, definition: list[str], expansion_factor: int = 2) -> None:
        self.map = [list(row) for row in definition]
        self.expanded_rows, self.expanded_cols = self.expand()
        self.galaxies = self.find_galaxies(expansion_factor - 1)

    def _transpose_map(self, map_2d: list[list[str]]) -> list[list[str]]:
        return list(zip(*map_2d))

    def expand(self) -> tuple[list[int], list[int]]:
        expanded_rows = []
        for i, row in enumerate(self.map):
            if all(c == "." for c in row):
                expanded_rows.append(i)
        expanded_cols = []
        for i, row in enumerate(self._transpose_map(self.map)):
            if all(c == "." for c in row):
                expanded_cols.append(i)
        return expanded_rows, expanded_cols

    def find_galaxies(self, expansion_factor: int) -> list[Galaxy]:
        galaxies = []
        for row, row_list in enumerate(self.map):
            for col, symbol in enumerate(row_list):
                if symbol == "#":
                    expanded_rows = [r for r in self.expanded_rows if r < row]
                    expanded_cols = [c for c in self.expanded_cols if c < col]
                    galaxies.append(
                        Galaxy(row + expansion_factor * len(expanded_rows), col + expansion_factor * len(expanded_cols))
                    )
        return galaxies


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_to_list
        self.parser_kwargs = dict(comment="N")

    def task(self, expansion_factor: int):
        universe = Universe(self.input, expansion_factor)
        # pprint(universe.galaxies)
        shortest_path_sum = 0
        for i, galaxy_1 in enumerate(universe.galaxies):
            for galaxy_2 in universe.galaxies[i + 1 :]:
                shortest_path_sum += galaxy_1 - galaxy_2
        return shortest_path_sum

    def task_1(self):
        return self.task(expansion_factor=2)

    def task_2(self, expansion_factor: int = 100):
        return self.task(expansion_factor)


part = 2
solve_example = True
solve_example = False
example_solutions = [374, 8410]

solver = Solver(year=2023, day=11)
# solve always all examples, but only one final task
if solve_example:
    for p in range(1, part + 1):
        solver.solve_examples(p, example_solutions[p - 1])
else:
    solver.task_2 = partial(solver.task_2, expansion_factor=1_000_000)
    solver.solve_task(part, verbose=False)
