from wrapper import Wrapper
from typing import List, Tuple, Set, Dict, Union  # noqa: F401
from itertools import zip_longest, chain
from functools import cmp_to_key
from pprint import pprint

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

    def compare(self, left: Union[List, int], right: Union[List, int]) -> int:
        """
        Return which item is smaller - `left` -> -1, `right` -> 1 or `tie` -> 0.
        """
        if left is None:  # left list was shorter
            return -1
        if right is None:
            return 1

        if type(left) == type(right) == int:
            if left < right:
                return -1
            elif left == right:
                return 0
            else:
                return 1

        if type(left) != type(right):
            if type(left) == int:
                left = [left]
            else:
                right = [right]

        # now both are lists
        for l, r in zip_longest(left, right):
            result = self.compare(l, r)
            if result != 0:
                return result
        else:
            return 0

    def task_1(self):
        correct_order = []
        for i, (left, right) in enumerate(self.input):
            # print(f'{left=}')
            # print(f'{right=}')
            # print(f'{self.compare(left, right)=}')
            # print()
            if self.compare(left, right) == -1:
                correct_order.append(i + 1)
        print(f"{correct_order=}")
        return sum(correct_order)

    def task_2(self):
        packets = list(chain.from_iterable(self.input))
        dividers = [[[2]], [[6]]]
        ordered = sorted(packets + dividers, key=cmp_to_key(self.compare))
        pprint(ordered)
        indices = [(d, ordered.index(d) + 1) for d in dividers]
        print(f"{indices=}")
        decoder_key = indices[0][1] * indices[1][1]
        return decoder_key


part = 2
solve_example = True
solve_example = False
example_solutions = [13, 140]

solver = Solver(day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
