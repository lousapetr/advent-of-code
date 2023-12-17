"""
--- Day 13: Point of Incidence ---

https://adventofcode.com/2023/day/13
"""

from pprint import pprint  # noqa: F401

from wrapper import Wrapper


def transpose(array: list[str]) -> list[str]:
    array_2d = [list(line) for line in array]
    transposed_array = zip(*array_2d)
    return ["".join(line) for line in transposed_array]


def find_reflection(array: list[str]) -> int:
    """
    Find horizontal reflection line.

    Returns:
        int: number of rows above a horizontal line of reflection
    """
    for i in range(1, len(array)):
        if array[i - 1] == array[i] and test_reflection(array, i):
            return i
    return 0


def test_reflection(array: list[str], reflection_line: int) -> bool:
    """
    Test whether a candidate `reflection_line` is a real mirror that reflects the array fully.

    Args:
        array (list[str]): pattern of lava
        reflection_line (int): number of lines above the reflection line

    Returns:
        bool: True if the reflection line mirrors the array perfectly.
    """
    mirrored_lines = zip(array[reflection_line:], array[reflection_line - 1 :: -1])
    return all(pair[0] == pair[1] for pair in mirrored_lines)


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom

    def parse_custom(self, path):
        with open(path) as f:
            patterns = f.read().split("\n\n")
        return [pattern.splitlines() for pattern in patterns]

    def task_1(self):
        patterns: list[list[str]] = self.input
        horizontal_mirrors = [find_reflection(pattern) for pattern in patterns]
        vertical_mirrors = [find_reflection(transpose(pattern)) for pattern in patterns]
        return sum(horizontal_mirrors) * 100 + sum(vertical_mirrors)

    def task_2(self):
        return NotImplemented


part = 1
solve_example = True
solve_example = False
example_solutions = [405, None]

solver = Solver(year=2023, day=13)
# solve always all examples, but only one final task
if solve_example:
    for p in range(1, part + 1):
        solver.solve_examples(p, example_solutions[p - 1])
else:
    solver.solve_task(part, verbose=False)
    solver.submit_answer(part)
