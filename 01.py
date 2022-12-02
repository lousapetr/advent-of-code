from wrapper import Wrapper

# https://adventofcode.com/2021/day/1


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_to_list
        self.input = super().load_input()

    def parse_custom(self, path):
        with open(path) as f:
            for line in f:
                pass

    def task_1(self):
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
        print(elf_calories)
        return max(elf_calories)

    def task_2(self):
        pass


part = 1
solve_example = False
example_solutions = [24_000, None]

solver = Solver(day=1, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)