"""
--- Day 24: Never Tell Me The Odds ---

https://adventofcode.com/2023/day/24
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import partial
from pprint import pprint  # noqa: F401
from typing import Optional

from wrapper import Wrapper


@dataclass
class Point:
    x: float
    y: float
    z: float

    def is_in_box(self, box_range: tuple[int, int], use_z: bool) -> bool:
        box_min, box_max = box_range
        return (
            (box_min <= self.x <= box_max)
            and (box_min <= self.y <= box_max)
            and (box_min <= self.z <= box_max or not use_z)
        )


@dataclass
class Hailstone:
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int

    def intersect_2d(self, other: Hailstone) -> Optional[Point]:
        """
        Find the future intersection of hailstones in 2D plane (i.e. with zero z-axis) for Part 1.

        If they move parallel or they intersected in the past, return None.
        """
        if abs(self.vx) == abs(other.vx) and abs(self.vy) == abs(other.vy):
            return None
        # self is on line y = self_a * x + self_b
        self_a = self.vy / self.vx
        self_b = self.y - self.x * self_a
        other_a = other.vy / other.vx
        other_b = other.y - other.x * other_a

        if self_a == other_a:  # parallel lines
            return

        intersect_x = (other_b - self_b) / (self_a - other_a)
        intersect_y = self_a * intersect_x + self_b
        intersect = Point(intersect_x, intersect_y, 0)

        if self.is_in_future(intersect) and other.is_in_future(intersect):
            return intersect
        return

    def is_in_future(self, point: Point) -> bool:
        return (point.x - self.x) / self.vx >= 0


class Solver(Wrapper):
    def __init__(self, **kwargs):
        self.input: list[Hailstone]
        super().__init__(**kwargs)
        self.parser = self.parse_custom

    def parse_custom(self, path):
        hailstones = []
        with open(path) as f:
            for line in f:
                numbers_str = re.findall(r"-?\d+", line)
                numbers = [int(n) for n in numbers_str]
                hailstones.append(Hailstone(*numbers))
        return hailstones

    def task_1(self, test_range: tuple[int, int] = (200000000000000, 400000000000000)) -> int:
        hailstones: list[Hailstone] = self.input
        collisions = 0
        for i, hailstone in enumerate(hailstones):
            for other in hailstones[i + 1 :]:
                intersect = hailstone.intersect_2d(other)
                # print(hailstone, other, intersect)
                if intersect and intersect.is_in_box(test_range, use_z=False):
                    collisions += 1
        return collisions

    def task_2(self):
        return NotImplemented


part = 2
solve_example = True
# solve_example = False
example_solutions = [2, 47]

solver = Solver(year=2023, day=24)
# solve always all examples, but only one final task
if solve_example:
    solver.task_1 = partial(solver.task_1, test_range=(7, 27))
    solver.solve_examples(1, example_solutions[0])
    if part == 2:
        solver.solve_examples(2, example_solutions[1])
else:
    solver.solve_task(part, verbose=False)
    solver.submit_answer(part)
