from __future__ import annotations
from wrapper import Wrapper
from typing import List, Tuple, Set, Dict, Optional  # noqa: F401
import re
from pprint import pprint
from dataclasses import dataclass

# https://adventofcode.com/2022/day/15

DAY_NUMBER = 15


@dataclass
class Rectangle:
    left_x: int
    right_x: int
    top_y: int
    bottom_y: int

    # def corners(self) -> List[Tuple[int, int]]:
    #     """
    #     :return: All four corners of rectangle from top left clockwise
    #     :rtype: List[Tuple[int, int]]
    #     """
    #     return [
    #         (self.left_x, self.top_y),
    #         (self.right_x, self.top_y),
    #         (self.right_x, self.bottom_y),
    #         (self.left_x, self.bottom_y)
    #     ]

    def __eq__(self, __o: Rectangle) -> bool:
        return (
            (self.left_x == __o.left_x)
            and (self.right_x == __o.right_x)
            and (self.top_y == __o.top_y)
            and (self.bottom_y == __o.bottom_y)
        )

    def __hash__(self) -> int:
        return hash((self.left_x, self.right_x, self.top_y, self.bottom_y))

    def contains(self, corner: Tuple[int, int]) -> bool:
        return (
            (self.left_x <= corner[0] <= self.right_x)
            and (self.bottom_y >= corner[1] >= self.top_y)
        )

    def cut(self, other: Rectangle) -> Set[Rectangle]:
        """
        `self` is yet unmapped rectangle, `other` defines rectangle covered by new beacon

        Each corner of `other` "cuts" into the unmapped area, splitting it into
        three new rectangles - one diagonally touching the corner, and two touching
        each side.

        0, 0 = top left corner
        """
        cuts = set()
        _sl, _sr, _st, _sb = self.left_x, self.right_x, self.top_y, self.bottom_y
        _ol, _or, _ot, _ob = other.left_x, other.right_x, other.top_y, other.bottom_y
        _slt = (_sl, _st)
        _srt = (_sr, _st)
        _slb = (_sl, _sb)
        _srb = (_sr, _sb)
        if all([  # self is completely covered by other
            other.contains(_slt),
            other.contains(_srt),
            other.contains(_slb),
            other.contains(_srb)
        ]):
            return set()
        if other.contains(_slt) and other.contains(_srt):  # other covers top half of self
            return {Rectangle(_sl, _sr, _ob + 1, _sb)}
        if other.contains(_slb) and other.contains(_srb):  # other covers bottom half of self
            return {Rectangle(_sl, _sr, _st, _ot - 1)}
        if other.contains(_slt) and other.contains(_slb):  # other covers left half of self
            return {Rectangle(_or + 1, _sr, _st, _sb)}
        if other.contains(_srt) and other.contains(_srb):  # other covers right half of self
            return {Rectangle(_sl, _ol - 1, _st, _sb)}
        # top left corner
        if self.contains((_ol, _ot)):
            cuts.add(Rectangle(_sl, _ol - 1, _st, _ot - 1))  # left top
            cuts.add(Rectangle(_sl, _ol - 1, _ot, min(_sb, _ob)))  # left
            cuts.add(Rectangle(_ol, min(_sr, _or), _st, _ot - 1))  # top
        # top right corner
        if self.contains((_or, _ot)):
            cuts.add(Rectangle(_or + 1, _sr, _st, _ot - 1))  # right top
            cuts.add(Rectangle(_or + 1, _sr, _ot, min(_ob, _sb)))  # right
            cuts.add(Rectangle(max(_ol, _sl), _or, _st, _ot - 1))  # top
        # bottom left corner
        if self.contains((_ol, _ob)):
            cuts.add(Rectangle(_sl, _ol - 1, _ob + 1, _sb))  # left bottom
            cuts.add(Rectangle(_sl, _ol - 1, max(_ot, _st), _ob))  # left
            cuts.add(Rectangle(_ol, min(_or, _sr), _ob + 1, _sb))  # bottom
        if self.contains((_or, _ob)):
            cuts.add(Rectangle(_or + 1, _sr, _ob + 1, _sb))  # right bottom
            cuts.add(Rectangle(_or + 1, _sr, max(_ot, _st), _ob))  # right
            cuts.add(Rectangle(max(_ol, _sl), _or, _ob + 1, _sb))  # bottom
        return cuts if cuts else {self}  # if no cuts were done, return original rectangle


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom

    @staticmethod
    def get_sensors_beacons(lines: List[str]) -> List[Tuple[int, int, int,int]]:
        output = []
        number = re.compile(r'=([-0-9]*)')
        for line in lines:
            sensor = re.findall(number, line)
            output.append(tuple(int(num) for num in sensor))
        return output

    def parse_custom(self, path) -> List[Tuple[int, int, int,int]]:
        lines = self.parse_to_list(path)
        return self.get_sensors_beacons(lines)

    @staticmethod
    def covered_range_at_y(sensor: Tuple[int, int, int, int], y: int) -> Optional[Tuple[int, int]]:
        sensor_x, sensor_y, beacon_x, beacon_y = sensor
        beacon_dist = abs(beacon_x - sensor_x) + abs(beacon_y - sensor_y)
        # print(f"{beacon_dist=}")
        sensor_dist = abs(sensor_y - y)
        half_row_coverage = max(beacon_dist - sensor_dist, 0)
        # print(f"{half_row_coverage=}")
        if half_row_coverage > 0:
            covered_range = sensor_x - half_row_coverage, sensor_x + half_row_coverage
        else:
            covered_range = None
        return covered_range

    @staticmethod
    def count_covered_positions(covered_ranges: List[Tuple[int, int]]) -> int:
        sorted_ranges = sorted(covered_ranges)
        # print(f"{sorted_ranges=}")
        covered_count = 0
        unioned_range = []
        current_range = sorted_ranges[0]
        for r in sorted_ranges[1:]:
            if current_range[1] < r[0]:
                unioned_range.append(current_range)
                current_range = r
            else:
                current_range = (current_range[0], max(current_range[1], r[1]))
        unioned_range.append(current_range)
        # print(f"{unioned_range=}")
        return sum(r[1] - r[0] for r in unioned_range)

    def task_1(self):
        sensors = self.input
        y = 10 if self.example else 2_000_000
        covered_ranges = []
        for s in sensors:
            if cover := self.covered_range_at_y(s, y):
                covered_ranges.append(cover)
            # print(f"{s=}")
            # print(f"{cover=}")
        # print(covered_ranges)
        return self.count_covered_positions(covered_ranges)

    @staticmethod
    def rotate_forward(x: int, y: int) -> Tuple[int, int]:
        return (x+y, x-y)

    @staticmethod
    def rotate_backward(x: int, y: int) -> Tuple[int, int]:
        return ((x + y) // 2, (x - y) // 2)

    def sensor2rectangle(self, sensor: Tuple[int, int, int, int]) -> Rectangle:
        sensor_x, sensor_y, beacon_x, beacon_y = sensor
        beacon_dist = abs(beacon_x - sensor_x) + abs(beacon_y - sensor_y)
        corners_diamond = {
            "left": (sensor_x, sensor_y - beacon_dist),
            "right": (sensor_x, sensor_y + beacon_dist),
            "top": (sensor_x - beacon_dist, sensor_y),
            "bottom": (sensor_x + beacon_dist, sensor_y)
        }
        corners_rotated = [self.rotate_forward(c[0], c[1]) for c in corners_diamond.values()]
        left = min(c[0] for c in corners_rotated)
        right = max(c[0] for c in corners_rotated)
        top = min(c[1] for c in corners_rotated)
        bottom = max(c[1] for c in corners_rotated)
        return Rectangle(left, right, top, bottom)

    def task_2(self):
        sensors = self.input
        limit = 20 if self.example else 4_000_000

        unmapped_area = {Rectangle(0, 2 * limit, -limit, limit)}
        for s in sensors:
            # print(f"{unmapped_area=}")
            sensed_rect = self.sensor2rectangle(s)
            # print(f"{s=}")
            print(f"{sensed_rect=}")
            updated_area = set()
            for r in unmapped_area:
                cuts = r.cut(sensed_rect)
                # print(f"{r=}")
                # pprint(f"{cuts=}")
                updated_area.update(cuts)
            unmapped_area = updated_area
            print()
        pprint(unmapped_area)
        result = 0
        for unmapped in unmapped_area:
            if unmapped.left_x == unmapped.right_x and unmapped.top_y == unmapped.bottom_y:
                print(unmapped)
                x, y = self.rotate_backward(unmapped.left_x, unmapped.top_y)
                print(f"{x=} {y=}")
                if 0 <= x <= limit and 0 <= y <= limit:
                    result = 4_000_000 * x + y
        return result


part = 2
solve_example = True
solve_example = False
example_solutions = [26, 56000011]

solver = Solver(
    day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions
)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
