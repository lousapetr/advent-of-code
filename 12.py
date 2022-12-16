from wrapper import Wrapper
from typing import List, Tuple, Set, Dict  # noqa: F401
from igraph import Graph
from pprint import pprint

# https://adventofcode.com/2022/day/12

DAY_NUMBER = 12


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse2map

    def idx2pos(self, idx: int) -> Tuple[int, int]:
        row = idx // self.ncols
        col = idx % self.ncols
        return row, col

    def pos2idx(self, pos: Tuple[int, int]) -> int:
        return pos[0] * self.ncols + pos[1]

    def neighbors(self, pos: Tuple[int, int]):
        r, c = pos
        up = max(r - 1, 0), c
        down = min(r + 1, self.nrows - 1), c
        left = r, max(c - 1, 0)
        right = r, min(c+1, self.ncols - 1)
        return tuple(set([up, down, left, right]) - set([pos]))

    def parse2map(self, path: str) -> List[str]:
        rows = self.parse_to_list(path)
        self.nrows = len(rows)
        self.ncols = len(rows[0])
        return rows

    def map2graph(self, heightmap: List[str]) -> Tuple[List[Tuple[int]], int, int]:
        edges = []
        start_idx, end_idx = -1, -1
        # print(f'{self.nrows=} {self.ncols=}')
        for i_row, row in enumerate(heightmap):
            for i_col, height in enumerate(row):
                pos = (i_row, i_col)
                idx = self.pos2idx(pos)
                if height == 'S':
                    height = 'a'
                    start_idx = idx
                elif height == 'E':
                    height = 'z'
                    end_idx = idx
                # print(f'{i_row=} {i_col=}')
                for neigh_pos in self.neighbors(pos):
                    h_dest = heightmap[neigh_pos[0]][neigh_pos[1]]
                    if h_dest == 'E':
                        h_dest = 'z'
                    if ord(h_dest) <= ord(height) + 1:
                        edges.append((idx, self.pos2idx(neigh_pos)))
        return edges, start_idx, end_idx

    def task_1(self):
        heightmap = self.input
        # print(f'{len(heightmap)=} {len(heightmap[0])=}')
        heightmap_flat = ''.join(heightmap)
        edges, start_idx, end_idx = self.map2graph(heightmap)
        print(f'{start_idx=} {end_idx=}')
        G = Graph(
            n=(self.nrows * self.ncols),
            edges=edges,
            directed=True
            )
        shortest_path = G.get_k_shortest_paths(v=start_idx, to=end_idx, k=1)
        # pprint([[self.idx2pos(i) for i in p] for p in shortest_path])
        # pprint([''.join(heightmap_flat[i] for i in p) for p in shortest_path])
        # pprint([''.join(f'{p}') for p in shortest_path])

        return len(shortest_path[0]) - 1

    def task_2(self):
        return NotImplemented


part = 1
solve_example = True
solve_example = False
example_solutions = [31, None]

solver = Solver(
    day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions
)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
