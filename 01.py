import re

from wrapper import Wrapper

# --- Day 1: Trebuchet?! ---
# https://adventofcode.com/2023/day/1

DAY_NUMBER = 1


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_to_list

    def task_1(self):
        digits = ["".join(filter(lambda x: x.isdigit(), line)) for line in self.input]
        numbers = [self.first_last(d) for d in digits]
        return sum(numbers)

    @staticmethod
    def find_digits(string: str) -> list[str]:
        number_names_raw = "one, two, three, four, five, six, seven, eight, nine"
        number_names = number_names_raw.replace(",", "").split()
        # https://stackoverflow.com/a/5616910
        # finds all occurences, including overlaps
        digits_raw = re.findall(f"""(?=({"|".join(number_names) + "|[0-9]"}))""", string)
        print(f"{digits_raw=}")
        digits = [d if d.isdigit() else str(number_names.index(d) + 1) for d in digits_raw]
        print(f"{digits=}")
        return digits

    @staticmethod
    def first_last(digits: str) -> int:
        return int(digits[0] + digits[-1])

    def task_2(self):
        digits = [self.find_digits(s) for s in self.input]
        numbers = [self.first_last(d) for d in digits]
        return sum(numbers)


part = 2

solve_example = True
solve_example = False
example_solutions = [142, 281]

solver = Solver(day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
# solver.solve_task(1)
if part > 1:
    solver.solve_task(2, verbose=False)
