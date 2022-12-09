from wrapper import Wrapper
from typing import List, Tuple, Set, Dict  # noqa: F401
import numpy as np

marek = __import__("08_marek")
MAREK_DEBUG = False

# https://adventofcode.com/2022/day/8

DAY_NUMBER = 8


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if MAREK_DEBUG:
            self.parser = self.parse_to_list
        else:
            self.parser = self.parse_to_array

    @staticmethod
    def find_visible_from_north(forest: np.ndarray) -> np.ndarray:
        visibility_matrix = np.zeros_like(forest).astype(bool)
        blocking = -1 * np.ones_like(forest[0])
        for i, row in enumerate(forest):
            row_visibility = row > blocking
            visibility_matrix[i] = row_visibility
            blocking = np.maximum(row, blocking)
            # if not any(row_visibility):
            #     break
        return visibility_matrix

    def visible(self, forest: np.ndarray) -> np.ndarray:
        total_visibility = np.zeros_like(forest).astype(bool)
        for rotation in range(4):
            rotated_forest = np.rot90(forest, rotation)
            print("-" * 30)
            # print(self.array_to_string(rotated_forest))
            # print()
            # print(self.array_to_string(np.rot90(rotated_forest, -rotation)))
            # print()
            north_visibility = self.find_visible_from_north(rotated_forest)
            # print(self.array_to_string(north_visibility.astype(int)))
            # print()
            visibility = np.rot90(north_visibility, -rotation)
            # self.print_visibility(forest, visibility)
            total_visibility = np.logical_or(total_visibility, visibility)
        return total_visibility

    def print_visibility(self, forest: np.ndarray, visibility: np.ndarray) -> None:
        visible_forest = forest * visibility
        visible_forest_str = self.array_to_string(visible_forest)
        pretty_forest = visible_forest_str.replace("0", ".")
        print(pretty_forest)

    def task_1(self):
        if MAREK_DEBUG:
            return marek.visible_trees(self.input)
        forest = self.input
        # print(self.array_to_string(forest))
        print()
        visibility = self.visible(forest)
        # print(self.array_to_string(visibility.astype(int)))
        # print()
        # self.print_visibility(forest, visibility)
        return np.sum(visibility.astype(int))

    def task_2(self):
        return NotImplemented


part = 1
solve_example = True
# solve_example = False
example_solutions = [(21, 1803, 1837), None]

solver = Solver(
    day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions
)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
