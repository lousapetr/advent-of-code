from typing import Dict, List, Set, Tuple  # noqa: F401

import numpy as np
import plotly.express as px
import plotly.graph_objects as go

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
        while position[1] < self.lowest_y:
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

    def show_scene_static(self):
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
        if self.example:
            height = 300
        if part == 1:
            height = 1500
        else:
            height = 800
        fig = px.imshow(matrix, height=height)
        fig.show()

    def prepare_data_movie(self, walls_history: List[Set], sand_history: List[Set]):
        sand_color = 5
        wall_color = 10
        x_min = min(min(w[0] for w in walls) for walls in walls_history)
        x_max = max(max(w[0] for w in walls) for walls in walls_history)
        y_max = self.lowest_y + 1
        matrix = [
            [[0 for x in range(x_min - 1, x_max + 1)] for y in range(-1, y_max + 1)] for t in range(len(walls_history))
        ]
        for time in range(len(walls_history)):
            matrix[time][0][500 - x_min] = sand_color  # origin
            for w_x, w_y in walls_history[time]:
                matrix[time][w_y][w_x - x_min] = wall_color
            for s_x, s_y in sand_history[time]:
                matrix[time][s_y][s_x - x_min] = sand_color
        return matrix

    def show_scene_movie(self, walls_history: List[Set], sand_history: List[Set]):
        matrix = self.prepare_data_movie(walls_history, sand_history)
        fig = px.imshow(np.array(matrix), height=800, animation_frame=0)
        fig.show()

    def show_scene_movie2(self, walls_history: List[Set], sand_history: List[Set]):
        matrix = self.prepare_data_movie(walls_history, sand_history)
        base = px.imshow(matrix[0], aspect="auto")

        frames = [
            go.Frame(
                data=px.imshow(matrix[i], aspect="auto").data,
                name=i,
            )
            for i in range(len(walls_history))
        ]

        fig = go.Figure(data=frames[1].data, frames=frames, layout=base.layout)
        fig.update_layout(
            updatemenus=[
                {
                    "buttons": [
                        {
                            "args": [None, {"frame": {"duration": 500, "redraw": True}}],
                            "label": "&#9654;",
                            "method": "animate",
                        },
                    ],
                    "type": "buttons",
                }
            ],
            sliders=[
                {
                    "steps": [
                        {
                            "args": [
                                [d],
                                {
                                    "frame": {"duration": 0, "redraw": True},
                                    "mode": "immediate",
                                },
                            ],
                            "label": d,
                            "method": "animate",
                        }
                        for d in range(0, len(walls_history))
                    ],
                }
            ],
        )
        fig.show()

    def task_1(self):
        self.walls = self.input
        self.lowest_y = max(w[1] for w in self.walls)
        while True:
            new_sand = self.drop_sand_grain()
            if new_sand[1] < self.lowest_y:
                self.sand.add(new_sand)
            else:
                # self.show_scene_static()
                return len(self.sand)

    def task_2(self):
        self.walls = self.input
        walls_history = []
        sand_history = []
        self.lowest_y = max(w[1] for w in self.walls) + 2
        x_min, x_max = min(w[0] for w in self.walls), max(w[0] for w in self.walls)
        self.walls.update({(x, self.lowest_y) for x in range(x_min - 1, x_max + 1)})
        while (500, 0) not in self.sand:
            new_sand = self.drop_sand_grain()
            if len(self.sand) % 10 == 0:
                #     print(f"{len(self.sand)=}")
                #     # self.show_scene()
                walls_history.append(self.walls)
                sand_history.append(self.sand)
            if new_sand[1] >= self.lowest_y:
                self.walls.add(new_sand)
                # print(f"Floor enlarged: {new_sand=}")
            else:
                self.sand.add(new_sand)
        self.show_scene_movie2(walls_history, sand_history)
        return len(self.sand)


part = 2
solve_example = True
# solve_example = False
example_solutions = [24, 93]

solver = Solver(day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
