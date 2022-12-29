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
        lava_cubes = set(self.input)
        # 1. create all "outside" air cells starting from far away by going through neighbors
        x_min, x_max = min(c[0] for c in lava_cubes) - 2, max(c[0] for c in lava_cubes) + 2
        y_min, y_max = min(c[1] for c in lava_cubes) - 2, max(c[1] for c in lava_cubes) + 2
        z_min, z_max = min(c[2] for c in lava_cubes) - 2, max(c[2] for c in lava_cubes) + 2
        outside: Set[CubeType] = set()
        to_visit = set([(x_min, y_min, z_min)])
        while to_visit:
            cube = to_visit.pop()
            if cube[0] in range(x_min, x_max) and cube[1] in range(y_min, y_max) and cube[2] in range(z_min, z_max):
                outside.add(cube)
                neighbors = self.neighbors_set(cube)
                new_visits = neighbors - outside - lava_cubes
                to_visit.update(new_visits)

        # 2. calculate intersection between neighbors of lava cubes and outside cells
        outside_surface = 0
        for cube in lava_cubes:
            neigbors = self.neighbors_set(cube)
            outside_neighbors = neigbors.intersection(outside)
            outside_surface += len(outside_neighbors)
        return outside_surface


part = 2
solve_example = True
solve_example = False
example_solutions = [64, 58]

solver = Solver(day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
