from wrapper import Wrapper

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
    def get_priority(letter: str) -> int:
        return (ord(letter) % 64 + 26) % 58

    def task_1(self):
        result = 0
        for r in self.input:
            parts = self.split_parts(r)
            common = set(parts[0]) & set(parts[1])
            result += self.get_priority(common.pop())
        return result

    def task_2(self):
        pass


part = 1
solve_example = False
example_solutions = [157, None]

solver = Solver(day=3, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)