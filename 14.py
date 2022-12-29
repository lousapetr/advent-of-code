from typing import Dict, List, Set, Tuple  # noqa: F401

import plotly.express as px

from wrapper import Wrapper

# https://adventofcode.com/2022/day/14

DAY_NUMBER = 14


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom
        self.walls: Set[Tuple[int, int]]
        self.sand: Set[Tuple[int, int]] = set()
        self.lowest_y: int

    def parse_custom(self, path) -> Set[Tuple[int, int]]:
        walls = set()
        with open(path) as f:
            for line in f:
                coords_str = line.strip().split(" -> ")
                coords_split = [c.split(",") for c in coords_str]
                coords = [(int(c[0]), int(c[1])) for c in coords_split]
                for i in range(len(coords) - 1):
                    first, last = coords[i], coords[i + 1]
                    if first[0] == last[0]:  # vertical wall
                        new_range = sorted([first[1], last[1]])
                        walls.update({(first[0], y) for y in range(new_range[0], new_range[1] + 1)})
                    if first[1] == last[1]:  # horizontal wall
                        new_range = sorted([first[0], last[0]])
                        walls.update({(x, first[1]) for x in range(new_range[0], new_range[1] + 1)})
        return set(walls)

    def drop_sand_grain(self) -> Tuple[int, int]:
        position = (500, 0)
        occupied = self.walls.union(self.sand)
        while position[1] <= self.lowest_y + 1:
            if not (new_pos := (position[0], position[1] + 1)) in occupied:  # down
                position = new_pos
            elif not (new_pos := (position[0] - 1, position[1] + 1)) in occupied:  # down-left
                position = new_pos
            elif not (new_pos := (position[0] + 1, position[1] + 1)) in occupied:  # down-right
                position = new_pos
            else:  # come to rest
                return position
        else:
            return position

    def show_scene(self):
        sand_color = 5
        wall_color = 10
        walls_long = list(zip(*self.walls))
        x_min, x_max = min(walls_long[0]) - 1, max(walls_long[0])
        _, y_max = min(walls_long[1]), max(walls_long[1])
        matrix = [[0 for x in range(x_min - 1, x_max + 1)] for y in range(-1, y_max + 1)]
        matrix[0][500 - x_min] = sand_color  # origin
        for w_x, w_y in self.walls:
            matrix[w_y][w_x - x_min] = wall_color
        for s_x, s_y in self.sand:
            matrix[s_y][s_x - x_min] = sand_color
        height = 1500 if not self.example else 300
        fig = px.imshow(matrix, height=height)
        fig.show()

    def task_1(self):
        self.walls = self.input
        self.lowest_y = max(w[1] for w in self.walls)
        while True:
            new_sand = self.drop_sand_grain()
            if new_sand[1] <= self.lowest_y:
                self.sand.add(new_sand)
            else:
                self.show_scene()
                return len(self.sand)

    def task_2(self):
        return NotImplemented


part = 1
solve_example = True
solve_example = False
example_solutions = [24, None]

solver = Solver(day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1, verbose=True)
if part > 1:
    solver.solve_task(2)
