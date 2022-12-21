from wrapper import Wrapper
from typing import List, Tuple, Set, Dict  # noqa: F401

# https://adventofcode.com/2022/day/18

DAY_NUMBER = 18

CubeType = Tuple[int, int, int]


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom

    def parse_custom(self, path) -> List[CubeType]:
        input_list = self.parse_to_list(path)
        input_tuples = [line.split(",") for line in input_list]
        return [tuple(int(n) for n in cube) for cube in input_tuples]

    @staticmethod
    def neighbors_set(cube: CubeType) -> Set[CubeType]:
        return {
            (cube[0] - 1, cube[1], cube[2]),
            (cube[0] + 1, cube[1], cube[2]),
            (cube[0], cube[1] - 1, cube[2]),
            (cube[0], cube[1] + 1, cube[2]),
            (cube[0], cube[1], cube[2] - 1),
            (cube[0], cube[1], cube[2] + 1),
        }

    def task_1(self):
        cubes = set(self.input)
        exposed_sides = 0
        for cube in cubes:
            neighbors = self.neighbors_set(cube)
            exposed_sides += len(neighbors - cubes)
        return exposed_sides

    def task_2(self):
        return NotImplemented


part = 1
solve_example = True
solve_example = False
example_solutions = [64, None]

solver = Solver(day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
