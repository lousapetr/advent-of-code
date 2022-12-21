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

    @staticmethod
    def decryption(input_list: List[int], mix_count: int) -> int:
        orig = [(i, n) for i, n in enumerate(input_list)]
        modifiable = orig.copy()
        for _ in range(mix_count):
            for item in orig:
                idx = modifiable.index(item)
                modifiable.pop(idx)
                new_idx = (idx + item[1]) % (len(orig) - 1)
                modifiable.insert(new_idx, item)
                # print(item, [n for _, n in modifiable])
        result_list = [n for _, n in modifiable]
        result_idx_start = result_list.index(0)
        result_indices = [(result_idx_start + i) % len(result_list) for i in (1000, 2000, 3000)]
        return sum(result_list[i] for i in result_indices)

    def task_1(self):
        return self.decryption(self.input, mix_count=1)

    def task_2(self):
        return self.decryption([n * 811589153 for n in self.input], mix_count=10)


part = 2
solve_example = True
solve_example = False
example_solutions = [3, 1623178306]

solver = Solver(day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
