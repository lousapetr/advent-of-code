from wrapper import Wrapper
from typing import List, Set

# https://adventofcode.com/2021/day/3


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_to_list
        self.input = super().load_input()

    @staticmethod
    def split_parts(rucksack: str):
        size = len(rucksack)
        part1, part2 = rucksack[: size // 2], rucksack[size // 2 :]
        assert len(part1) == len(part2)
        return part1, part2

    @staticmethod
    def get_common(rucksacks: List[str]) -> str:
        return set.intersection(*[set(r) for r in rucksacks]).pop()

    @staticmethod
    def get_priority(letter: str) -> int:
        return (ord(letter) % 64 + 26) % 58

    def task_1(self):
        result = 0
        for r in self.input:
            parts = self.split_parts(r)
            common = self.get_common(parts)
            result += self.get_priority(common)
        return result

    def task_2(self):
        result = 0
        for i in range(0, len(self.input), 3):
            common = self.get_common(self.input[i : i + 3])
            result += self.get_priority(common)
        return result


part = 2
solve_example = False
example_solutions = [157, 70]

solver = Solver(day=3, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)