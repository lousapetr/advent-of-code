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


def find_reflection(array: list[str], with_smudge: bool = False) -> int:
    """
    Find horizontal reflection line.

    Returns:
        int: number of rows above a horizontal line of reflection
    """
    if with_smudge:
        test_reflection = test_reflection_with_smudge
    else:
        test_reflection = test_reflection_perfect
    for i in range(1, len(array)):
        if test_reflection(array, i):
            return i
    return 0


def test_reflection_perfect(array: list[str], reflection_line: int) -> bool:
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


def test_reflection_with_smudge(array: list[str], reflection_line: int) -> bool:
    """
    Test whether a candidate `reflection_line` is a real mirror that reflects the array with a single smudge.

    Args:
        array (list[str]): pattern of lava
        reflection_line (int): number of lines above the reflection line

    Returns:
        bool: True if the reflection line mirrors the array exactly with a single smudge.
    """
    mirrored_lines = "".join(array[reflection_line:]), "".join(array[reflection_line - 1 :: -1])
    differences = list(filter(lambda pair: pair[0] != pair[1], zip(*mirrored_lines)))
    return len(differences) == 1


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom

    def parse_custom(self, path):
        with open(path) as f:
            patterns = f.read().split("\n\n")
        return [pattern.splitlines() for pattern in patterns]

    def task(self, with_smudge: bool) -> int:
        patterns: list[list[str]] = self.input
        horizontal_mirrors = [find_reflection(pattern, with_smudge) for pattern in patterns]
        vertical_mirrors = [find_reflection(transpose(pattern), with_smudge) for pattern in patterns]
        return sum(horizontal_mirrors) * 100 + sum(vertical_mirrors)

    def task_1(self):
        return self.task(with_smudge=False)

    def task_2(self):
        return self.task(with_smudge=True)


part = 2
solve_example = True
solve_example = False
example_solutions = [405, 400]

solver = Solver(year=2023, day=13)
# solve always all examples, but only one final task
if solve_example:
    for p in range(1, part + 1):
        solver.solve_examples(p, example_solutions[p - 1])
else:
    solver.solve_task(part, verbose=False)
    solver.submit_answer(part)
