from typing import Dict, List, Set, Tuple  # noqa: F401

from wrapper import Wrapper

# --- Day 25: Full of Hot Air ---
# https://adventofcode.com/2022/day/25

DAY_NUMBER = 25

SNAFU_BASE: int = 5
SNAFU_DIGITS = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
SNAFU_DIGITS_REVERSED = {(v % SNAFU_BASE): k for k, v in SNAFU_DIGITS.items()}


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_to_list

    def to_snafu(self, num: int) -> str:
        digits = []
        while num >= 1:
            pental_digit = num % SNAFU_BASE
            digits.insert(0, SNAFU_DIGITS_REVERSED[pental_digit])
            num //= SNAFU_BASE
            if pental_digit >= 3:
                num += 1
        return "".join(digits)

    def test_to_snafu(self):
        for decimal, snafu in [
            (10, "20"),
            (5, "10"),
            (3, "1="),
            (4, "1-"),
            (15, "1=0"),
            (20, "1-0"),
            (2022, "1=11-2"),
            (314159265, "1121-1110-1=0"),
        ]:
            result = self.to_snafu(decimal)
            print(f"{decimal=}\t{snafu=}\t{result=}")
            assert result == snafu

    def from_snafu(self, snafu: str) -> int:
        result = 0
        for i, c in enumerate(snafu[::-1]):
            digit = SNAFU_DIGITS[c]
            result += digit * SNAFU_BASE**i
        return result

    def task_1(self):
        self.test_to_snafu()
        converted = [self.from_snafu(n) for n in self.input]
        print(converted)
        print(f"{sum(converted)=}")
        return self.to_snafu(sum(converted))

    def task_2(self):
        return NotImplemented


part = 1
solve_example = True
solve_example = False
example_solutions = ["2=-1=0", None]

solver = Solver(day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
