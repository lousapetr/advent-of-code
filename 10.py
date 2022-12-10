from wrapper import Wrapper
from typing import List, Tuple, Set, Dict  # noqa: F401

# https://adventofcode.com/2022/day/10

DAY_NUMBER = 10

DEBUG = False


class CPU:
    def __init__(self, instructions: list[str]) -> None:
        self.registers = {"X": 1}
        self.tick_current = 1
        self.total_signal_strength = 0
        self.screen = ["." for _ in range(240)]
        self.instructions = instructions

    def run(self):
        for inst in self.instructions:
            inst = inst.strip()
            if inst == "noop":
                self.noop()
                continue
            op, value_str = inst.split()
            value = int(value_str)
            if op == "addx":
                self.addx(value)
                continue

    def get_total_signal_strength(self) -> int:
        return self.total_signal_strength

    def render_screen(self):
        for idx in range(40, 241, 40):
            print("".join(self.screen[(idx - 40) : idx]))

    def _tick(self):
        if self.tick_current in range(20, 221, 40):
            signal = self.registers["X"] * self.tick_current
            self.total_signal_strength += signal

        crt_position = (self.tick_current - 1) % 240
        if abs(crt_position % 40 - self.registers["X"]) <= 1:
            self.screen[crt_position] = "#"
        else:
            self.screen[crt_position] = "."

        if DEBUG and self.tick_current < 22:
            print(
                f"End of cycle {self.tick_current - 1}: (Register X is now {self.registers['X']})"
            )
            print()
            print(
                f"During cycle {self.tick_current}: CRT draws pixel in position {crt_position}"
            )
            print(f"Current CRT row: {''.join(self.screen[:40])}")

        self.tick_current += 1

    def noop(self):
        self._tick()

    def addx(self, value: int):
        self._tick()
        self._tick()
        self.registers["X"] += value


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_to_list

    def task_1(self):
        cpu = CPU(self.input)
        cpu.run()
        return cpu.get_total_signal_strength()

    def task_2(self):
        cpu = CPU(self.input)
        cpu.run()
        cpu.render_screen()


part = 2
solve_example = True
solve_example = False
example_solutions = [13140, None]

solver = Solver(
    day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions
)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2, verbose=True)  # BRJLFULP
