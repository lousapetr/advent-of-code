"""
--- Day 10: Pipe Maze ---

https://adventofcode.com/2023/day/10
"""

from dataclasses import dataclass
from pprint import pprint  # noqa: F401
from typing import Optional

from wrapper import Wrapper

Position = tuple[int, int]  # row, col


@dataclass
class Pipe:
    symbol: str
    pos: Position

    @property
    def north(self) -> Position:
        return self.pos[0] - 1, self.pos[1]

    @property
    def south(self) -> Position:
        return self.pos[0] + 1, self.pos[1]

    @property
    def west(self) -> Position:
        return self.pos[0], self.pos[1] - 1

    @property
    def east(self) -> Position:
        return self.pos[0], self.pos[1] + 1

    def other_end(self, input_pos: Position) -> Optional[Position]:
        """
        Find the other end of the pipe, given an entrance to `input_pos`.
        The pipe `self` connects the positions `input_pos` and the returned Position.

        Args:
            input_pos: position of entrance

        Returns:
            Position: row and col of the exit
                return None if the piping is not connected
        """
        # if not (input_row, input_col) in (self.north, self.south, self.west, self.east):
        # pipes only connect if directly attached
        # return None
        N, S, W, E = self.north, self.south, self.west, self.east
        connections = {"|": (N, S), "-": (W, E), "L": (N, E), "J": (N, W), "7": (S, W), "F": (S, E)}
        mappings = {(symbol, conn[0]): conn[1] for symbol, conn in connections.items()}
        mappings.update({(symbol, conn[1]): conn[0] for symbol, conn in connections.items()})
        return mappings.get((self.symbol, input_pos), None)


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_to_list
        self.parser_kwargs = {"astype": list}

    def create_2d_plan(self, array: list[list[str]]) -> dict[Position, Pipe]:
        plan = {}
        for num_row, row in enumerate(array):
            for num_col, symbol in enumerate(row):
                pos = (num_row, num_col)
                plan[pos] = Pipe(symbol, pos)
        return plan

    def task_1(self):
        plan = self.create_2d_plan(self.input)
        # print(self.array_to_string(self.input))
        loop: list[Pipe] = [p for p in plan.values() if p.symbol == "S"]
        start = loop[0]
        for neighbor in (start.north, start.south, start.west, start.east):
            if plan[neighbor].other_end(start.pos) is not None:
                loop.append(plan[neighbor])
                break
        while loop[-1] != start:
            if new_pos := loop[-1].other_end(loop[-2].pos):
                loop.append(plan[new_pos])
        return len(loop) // 2

    def task_2(self):
        return NotImplemented


part = 1
solve_example = True
solve_example = False
example_solutions = [(4, 8), None]

solver = Solver(year=2023, day=10)
# solve always all examples, but only one final task
if solve_example:
    for p in range(1, part + 1):
        solver.solve_examples(p, example_solutions[p - 1])
else:
    solver.solve_task(part, verbose=False)
