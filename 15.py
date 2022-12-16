from wrapper import Wrapper
from typing import List, Tuple, Set, Dict, Optional  # noqa: F401
import re
from pprint import pprint

# https://adventofcode.com/2022/day/15

DAY_NUMBER = 15


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
        print(f"{sorted_ranges=}")
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
        print(f"{unioned_range=}")
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
        print(covered_ranges)
        return self.count_covered_positions(covered_ranges)

    def task_2(self):
        return NotImplemented


part = 2
solve_example = True
# solve_example = False
example_solutions = [26, 56000011]

solver = Solver(
    day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions
)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
