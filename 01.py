from wrapper import Wrapper

# https://adventofcode.com/2021/day/1


class Solver(Wrapper):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom
        self.input = super().load_input()

    def parse_custom(self, path):
        with open(path) as f:
            for line in f:
                pass

    def task_1(self):
        pass

    def task_2(self):
        pass


part = 1
solve_example = True
example_solutions = [MISSING, None]

solver = Solver(day=1, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)