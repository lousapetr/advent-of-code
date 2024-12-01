"""
--- Day 15: Lens Library ---

https://adventofcode.com/2023/day/15
"""

from collections import OrderedDict
from pprint import pprint  # noqa: F401

from wrapper import Wrapper


class LightFacility:
    def __init__(self) -> None:
        self.boxes = [Box() for _ in range(256)]

    def apply_instruction(self, instruction: str) -> None:
        if "-" in instruction:
            label = instruction[:-1]
            self.boxes[self.hash(label)].remove_lens(label)
        elif "=" in instruction:
            label, focal_length_str = instruction.split("=")
            self.boxes[self.hash(label)].update_lens(label, int(focal_length_str))

    def focusing_power(self) -> int:
        return sum((box_num + 1) * box.focusing_power() for box_num, box in enumerate(self.boxes))

    @staticmethod
    def hash(string: str) -> int:
        value = 0
        for c in string:
            value += ord(c)
            value *= 17
            value %= 256
        return value

    def __str__(self) -> str:
        result = ""
        for i, box in enumerate(self.boxes):
            if box:
                result += f"Box {i}: {box.lenses}\n"
        return result


class Box:
    def __init__(self) -> None:
        self.lenses = OrderedDict()

    def __bool__(self) -> bool:
        return bool(self.lenses)

    def remove_lens(self, label: str) -> None:
        self.lenses.pop(label, None)

    def update_lens(self, label: str, focal_length: int) -> None:
        self.lenses[label] = focal_length

    def focusing_power(self) -> int:
        result = 0
        for slot, focal_length in enumerate(self.lenses.values()):
            result += (slot + 1) * focal_length
        return result


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom

    def parse_custom(self, path):
        with open(path) as f:
            return f.readline().strip().split(",")

    def task_1(self):
        assert LightFacility.hash("HASH") == 52
        hashes = [LightFacility.hash(s) for s in self.input]
        return sum(hashes)

    def task_2(self):
        facility = LightFacility()
        for instruction in self.input:
            facility.apply_instruction(instruction)
            print(f"After '{instruction}':")
            print(facility)
            print()
        return facility.focusing_power()


part = 2
solve_example = True
solve_example = False
example_solutions = [1320, 145]

solver = Solver(year=2023, day=15)
# solve always all examples, but only one final task
if solve_example:
    for p in range(1, part + 1):
        solver.solve_examples(p, example_solutions[p - 1])
else:
    solver.solve_task(part, verbose=False)
