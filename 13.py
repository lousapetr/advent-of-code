from wrapper import Wrapper
from typing import List, Tuple, Set, Dict, Union  # noqa: F401
from itertools import zip_longest

# https://adventofcode.com/2022/day/13

DAY_NUMBER = 13


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom

    def parse_custom(self, path):
        pairs = []
        pair = []
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line:
                    pair.append(eval(line))
                if len(pair) == 2:
                    pairs.append(pair)
                    pair = []
        return pairs

    def compare(self, left: Union[List, int], right: Union[List, int]) -> str:
        """
        Return which item is smaller - `left`, `right` or `tie`.
        """
        if left is None:  # left list was shorter
            return 'left'
        if right is None:
            return 'right'

        if type(left) == type(right) == int:
            if left < right:
                return 'left'
            elif left == right:
                return 'tie'
            else:
                return 'right'

        if type(left) != type(right):
            if type(left) == int:
                left = [left]
            else:
                right = [right]

        # now both are lists
        for l, r in zip_longest(left, right):
            result = self.compare(l, r)
            if result != 'tie':
                return result
        else:
            return 'tie'


    def task_1(self):
        correct_order = []
        for i, (left, right) in enumerate(self.input):
            print(f'{i:3d} / {len(self.input)}', end='\r')
            # print(f'{left=}')
            # print(f'{right=}')
            # print(f'{self.compare(left, right)=}')
            # print()
            if self.compare(left, right) == 'left':
                correct_order.append(i + 1)
        print(f'{correct_order=}')
        return sum(correct_order)

    def task_2(self):
        return NotImplemented


part = 1
solve_example = True
solve_example = False
example_solutions = [13, None]

solver = Solver(
    day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions
)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
