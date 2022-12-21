from wrapper import Wrapper
from typing import List, Tuple, Set, Dict  # noqa: F401

# https://adventofcode.com/2022/day/20

DAY_NUMBER = 20


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom

    def parse_custom(self, path):
        return [int(n) for n in self.parse_to_list(path)]

    def task_1(self):
        orig = [(i, n) for i, n in enumerate(self.input)]
        modifiable = orig.copy()
        for item in orig:
            idx = modifiable.index(item)
            modifiable.pop(idx)
            new_idx = (idx + item[1]) % (len(orig) - 1)
            # new_idx = new_idx % len(orig) if new_idx >= 0 else (new_idx - 1) % len(orig)
            modifiable.insert(new_idx, item)
            print(item, [n for _, n in modifiable])
        result_list = [n for _, n in modifiable]
        result_idx_start = result_list.index(0)
        result_indices = [(result_idx_start + i) % len(result_list) for i in (1000, 2000, 3000)]
        # return modifiable[1000 % len(orig)][1] + modifiable[2000 % len(orig)][1] + modifiable[3000 % len(orig)][1]
        return sum(result_list[i] for i in result_indices)

    def task_2(self):
        return NotImplemented


part = 1
solve_example = True
solve_example = False
example_solutions = [3, None]

solver = Solver(day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
