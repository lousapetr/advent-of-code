"""
--- Day 15: Lens Library ---

https://adventofcode.com/2023/day/15
"""

from pprint import pprint  # noqa: F401

from wrapper import Wrapper


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom

    def parse_custom(self, path):
        with open(path) as f:
            return f.readline().strip().split(",")

    def hash(self, string: str) -> int:
        value = 0
        for c in string:
            value += ord(c)
            value *= 17
            value %= 256
        return value

    def task_1(self):
        assert self.hash("HASH") == 52
        hashes = [self.hash(s) for s in self.input]
        return sum(hashes)

    def task_2(self):
        return NotImplemented


part = 2
solve_example = True
# solve_example = False
example_solutions = [1320, 145]

solver = Solver(year=2023, day=15)
# solve always all examples, but only one final task
if solve_example:
    for p in range(1, part + 1):
        solver.solve_examples(p, example_solutions[p - 1])
else:
    solver.solve_task(part, verbose=False)
