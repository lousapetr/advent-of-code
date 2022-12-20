from wrapper import Wrapper

# https://adventofcode.com/2021/day/1


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_to_list
        self.input = super().load_input()
        self.calories_per_elf = self.get_calories_per_elf()

    def parse_custom(self, path):
        with open(path) as f:
            for line in f:
                pass

    def get_calories_per_elf(self):
        elf_calories = []
        single_elf_cals = 0
        for item in self.input:
            if item:
                single_elf_cals += int(item)
            else:
                elf_calories.append(single_elf_cals)
                single_elf_cals = 0
                continue
        elf_calories.append(single_elf_cals)
        return elf_calories

    def task_1(self):
        return max(self.calories_per_elf)

    def task_2(self):
        return sum(sorted(self.calories_per_elf)[-3:])


part = 2
solve_example = False
example_solutions = [24_000, 45000]

solver = Solver(day=1, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
