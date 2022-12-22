from typing import Dict, List, Set, Tuple  # noqa: F401

from wrapper import Wrapper

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
        cubes = set(self.input)
        neigbors = []
        for cube in cubes:
            neigbors.append(list(self.neighbors_set(cube)))
        # 1. add second layer of neighbors
        # 2. create graph of "water" cubes - vertices are cubes, edges are touching sides
        # 3. find connected components https://igraph.org/python/versions/latest/api/igraph.Graph.html#components
        # 4. there *should* be a single large component on the true outside and smaller (multiple?) components inside
        # 5. count all touching points between the large component and lava cubes


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