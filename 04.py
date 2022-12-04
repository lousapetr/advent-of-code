from wrapper import Wrapper
from typing import List, Tuple, Set, Dict

# https://adventofcode.com/2021/day/4


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom
        self.input = super().load_input()

    def parse_custom(self, path):
        result = []
        with open(path) as f:
            for line in f:
                line = line.strip()
                line_split = line.replace("-", ",").split(",")
                nums = [int(n) for n in line_split]
                sections = nums[:2], nums[2:]
                result.append(sections)
        return result

    @staticmethod
    def contains(sections: List[Tuple[int, int]]) -> bool:
        left, right = sections
        if left[0] >= right[0] and left[1] <= right[1]:
            return True  # right fully contains left
        if left[0] <= right[0] and left[1] >= right[1]:
            return True  # left fully contains right
        return False

    def task_1(self):
        return sum(map(self.contains, self.input))

    def task_2(self):
        pass


part = 1
solve_example = False
example_solutions = [2, None]

solver = Solver(day=4, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)