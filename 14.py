"""
--- Day 14: Parabolic Reflector Dish ---

https://adventofcode.com/2023/day/14
"""

from enum import Enum
from pprint import pprint  # noqa: F401

from wrapper import Wrapper

Plane = list[str]


class Direction(Enum):
    NORTH = 1
    WEST = 2
    SOUTH = 3
    EAST = 4


def transpose(plane: Plane) -> Plane:
    array_transposed = zip(*plane)
    return ["".join(row) for row in array_transposed]


def slide(plane: Plane, direction: Direction) -> Plane:
    if direction in (Direction.NORTH, Direction.SOUTH):
        plane = transpose(plane)
    reverse_sort = direction in (Direction.NORTH, Direction.WEST)
    rounded = [row.split("#") for row in plane]
    slided_rounds = [["".join(sorted(round_stretch, reverse=reverse_sort)) for round_stretch in row] for row in rounded]
    slided_plane = ["#".join(row) for row in slided_rounds]
    if direction in (Direction.NORTH, Direction.SOUTH):
        slided_plane = transpose(slided_plane)
    return slided_plane


def slide_cycle(plane: Plane) -> Plane:
    for d in Direction:
        plane = slide(plane, d)
    return plane


def total_load(plane: Plane) -> int:
    plane_size = len(plane)
    load = 0
    for i, row in enumerate(plane):
        load += (plane_size - i) * row.count("O")
    return load


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_to_list
        self.input: Plane

    def task_1(self):
        plane_slided_north = slide(self.input, Direction.NORTH)
        print(self.array_to_string(plane_slided_north))
        return total_load(plane_slided_north)

    def task_2(self):
        cycles_total = 1_000_000_000
        # cycles_total = 11
        plane = "\n".join(self.input)
        cycle_num = 0
        seen_configurations = {}
        # find when the sequence starts to repeat
        while plane not in seen_configurations:
            seen_configurations[plane] = cycle_num
            cycle_num += 1
            plane = "\n".join(slide_cycle(plane.split("\n")))
            # print(cycle_num, plane, sep="\n", end="\n\n")

        # print(f"{cycle_num=}")
        # print(f"{seen_configurations[plane]=}")
        # next_plane = "\n".join(slide_cycle(plane.split("\n")))
        # print(f'{seen_configurations[next_plane]=}')

        supercycle_start = seen_configurations[plane]
        supercycle_len = cycle_num - supercycle_start
        supercycle_count = (cycles_total - supercycle_start) // supercycle_len
        last_cycles_count = cycles_total - supercycle_len * supercycle_count
        last_plane = {v: k for k, v in seen_configurations.items()}[last_cycles_count]
        print(f"{supercycle_start=:,}")
        print(f"{supercycle_len=:,}")
        print(f"{last_cycles_count=:,}")
        print()
        # print(last_plane)
        return total_load(last_plane.split("\n"))


part = 2
solve_example = True
solve_example = False
example_solutions = [136, 64]

solver = Solver(year=2023, day=14)
# solve always all examples, but only one final task
if solve_example:
    for p in range(1, part + 1):
        solver.solve_examples(p, example_solutions[p - 1])
else:
    solver.solve_task(part, verbose=True)
    solver.submit_answer(part)
