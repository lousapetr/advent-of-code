from typing import Dict, List, Set, Tuple  # noqa: F401

import numpy as np
import numpy.typing as npt

from wrapper import Wrapper

# --- Day 24: Blizzard Basin ---
# https://adventofcode.com/2022/day/24

DAY_NUMBER = 24

PositionType = Tuple[int, int]  # row, col
MapType = npt.NDArray[np.int_]


class BlizzardBasin:
    def __init__(self, lines) -> None:
        self.positions: Set[PositionType]
        self.original_entry: PositionType
        self.destination: PositionType
        self.up: MapType
        self.down: MapType
        self.right: MapType
        self.left: MapType
        self.parse_lines(lines)

    def parse_lines(self, lines: List[str]):
        entry = lines[0].index(".") - 1
        self.original_entry = (-1, entry)
        self.positions = {self.original_entry}
        destination = lines[-1].index(".") - 1
        self.destination = (len(lines) - 2, destination)
        row_count = len(lines) - 2
        col_count = len(lines[0]) - 2
        self.up, self.down, self.right, self.left = [
            np.zeros(shape=(row_count, col_count), dtype=int) for _ in range(4)
        ]
        for row, line in enumerate(lines[1:-1]):
            for col, char in enumerate(line[1:-1]):
                if char == "^":
                    self.up[row, col] = 1
                if char == "v":
                    self.down[row, col] = 1
                if char == ">":
                    self.right[row, col] = 1
                if char == "<":
                    self.left[row, col] = 1

    def move_blizzards(self):
        self.up = np.roll(self.up, -1, axis=0)
        self.down = np.roll(self.down, 1, axis=0)
        self.right = np.roll(self.right, 1, axis=1)
        self.left = np.roll(self.left, -1, axis=1)

    def __str__(self) -> str:
        rows = []
        upper_wall = "".join("." if i == self.original_entry[1] + 1 else "#" for i in range(self.up.shape[1] + 2))
        bottom_wall = "".join("." if i == self.destination[1] + 1 else "#" for i in range(self.up.shape[1] + 2))
        rows = [upper_wall]
        all_dirs = self.up + self.down + self.right + self.left
        blizzard_map = np.zeros_like(all_dirs, dtype=str)
        for i, row in enumerate(all_dirs):
            for j, blizzard_count in enumerate(row):
                if blizzard_count == 0:
                    blizzard_map[i, j] = "."
                elif blizzard_count > 1:
                    blizzard_map[i, j] = blizzard_count
                else:
                    if self.up[i, j]:
                        blizzard_map[i, j] = "^"
                    if self.down[i, j]:
                        blizzard_map[i, j] = "v"
                    if self.right[i, j]:
                        blizzard_map[i, j] = ">"
                    if self.left[i, j]:
                        blizzard_map[i, j] = "<"
        rows = [upper_wall] + ["#" + "".join(row) + "#" for row in blizzard_map] + [bottom_wall]

        return "\n".join(rows)


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom

    def parse_custom(self, path) -> BlizzardBasin:
        with open(path) as f:
            return BlizzardBasin(lines=[r.strip() for r in f.readlines()])

    def task_1(self):
        blizzard_basin = self.input
        print(blizzard_basin)
        # for i in range(6):
        #     print(f"After minute {i}")
        #     print(blizzard_basin)
        #     blizzard_basin.move_blizzards()
        #     print()
        return NotImplemented

    def task_2(self):
        return NotImplemented


part = 1
solve_example = True
# solve_example = False
example_solutions = [
    (
        10,
        # 18,
    ),
    None,
]

solver = Solver(day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
