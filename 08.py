from wrapper import Wrapper
from typing import List, Tuple, Set, Dict, Sequence  # noqa: F401
import numpy as np
from numpy.typing import NDArray

marek = __import__("08_marek")
MAREK_DEBUG = False

# https://adventofcode.com/2022/day/8

DAY_NUMBER = 8


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.verbose = False
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

    @staticmethod
    def sight_lines(
        forest: NDArray[np.int_], row: int, col: int
    ) -> Sequence[NDArray[np.int_]]:
        right = forest[row, (col + 1) :]
        left = forest[row, (col - 1) :: -1]
        up = forest[(row - 1) :: -1, col]
        down = forest[(row + 1) :, col]
        return right, left, up, down

    def sight_range(self, height: int, line: NDArray[np.int_]) -> int:
        if line.size == 0:
            return 0
        visible_line = height > line
        if self.verbose:
            print(visible_line)
        if np.all(visible_line):
            return len(visible_line)
        return int(visible_line.argmin() + 1)  # find index of first False

    def scenic_score(self, forest: NDArray[np.int_], row: int, col: int) -> int:
        if row == 0 or col == 0:
            return 0
        tree_height = forest[row, col]
        score = 1
        for line in self.sight_lines(forest, row, col):
            sight = self.sight_range(tree_height, line)
            score *= sight
            if self.verbose:
                print(score, line, sight)
        return score

    def best_scenic_score(self, forest: NDArray[np.int_]) -> int:
        best_score = 0
        for row_idx, row in enumerate(forest):
            for col_idx, tree in enumerate(row):
                # if (row_idx, col_idx) == (2, 0):
                # self.verbose = True
                score = self.scenic_score(forest, row_idx, col_idx)
                if score > best_score:
                    best_score = score
                self.verbose = False
        return best_score

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
        return self.best_scenic_score(forest=self.input)


part = 2
solve_example = True
solve_example = False
example_solutions = [
    (21, 1803, 1837),
    (8, 268912),
]

solver = Solver(
    day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions
)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
