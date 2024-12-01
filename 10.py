"""
--- Day 10: Pipe Maze ---

https://adventofcode.com/2023/day/10
"""

from collections import OrderedDict
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

    def __str__(self) -> str:
        box_plotting = {"F": "╔", "|": "║", "L": "╚", "7": "╗", "J": "╝", "-": "═", "S": "S", ".": "."}
        return box_plotting[self.symbol]


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_to_list
        # self.parser_kwargs = {"astype": list}

    def create_2d_plan(self, array: list[list[str]]) -> OrderedDict[Position, Pipe]:
        plan = OrderedDict()
        for num_row, row in enumerate(array):
            for num_col, symbol in enumerate(row):
                pos = (num_row, num_col)
                plan[pos] = Pipe(symbol, pos)
        return plan

    def find_loop(self, plan: OrderedDict[Position, Pipe], start: Pipe) -> list[Position]:
        loop: list[Position] = [start.pos]
        # find first pipe after start
        for neighbor in (start.north, start.south, start.west, start.east):
            if -1 in neighbor:
                continue
            if plan[neighbor].other_end(start.pos) is not None:
                loop.append(neighbor)
                break
        # follow the loop
        while loop[-1] != start.pos:
            if new_pos := plan[loop[-1]].other_end(loop[-2]):
                loop.append(new_pos)
        return loop[:-1]

    def find_start(self, plan: OrderedDict[Position, Pipe]) -> Pipe:
        for p in plan.values():
            if p.symbol == "S":
                return p

    def print_input(self):
        return ""

    def task_1(self):
        plan = self.create_2d_plan(self.input)
        start = self.find_start(plan)
        loop = self.find_loop(plan, start)
        self.print_plan(plan, loop)
        return len(loop) // 2

    def print_plan(self, plan, loop, inside_places=[]) -> None:
        result = ""
        for pos, place in plan.items():
            if pos[1] == 0:
                result += "\n"
            if pos in loop:
                result += str(place)
            elif place in inside_places:
                result += "X"
            else:
                result += "."
        print(result)

    def task_2(self):
        plan = self.create_2d_plan(self.input)
        start = self.find_start(plan)
        loop = self.find_loop(plan, start)
        inside_places = []
        is_inside = False
        last_corner = ""
        # detect configuration of Start
        for configuration in "LFJ7|-":
            start.symbol = configuration
            print(f"{start.symbol=}")
            if start.other_end(loop[1]) == loop[-1]:
                plan[start.pos] = start
                break

        for position, place in plan.items():
            if position[1] == 0:
                is_inside = False
            if position not in loop:
                if is_inside:
                    inside_places.append(place)
            elif place.symbol == "|":
                is_inside = not is_inside
            elif place.symbol in "LF":
                last_corner = place.symbol
            elif (place.symbol == "J" and last_corner == "F") or (place.symbol == "7" and last_corner == "L"):
                last_corner = ""
                is_inside = not is_inside
        self.print_plan(plan, loop, inside_places)
        return len(inside_places)


part = 2
solve_example = True
solve_example = False
example_solutions = [(4, 8), (1, 1, 4, 8, 10)]

solver = Solver(year=2023, day=10)
# solve always all examples, but only one final task
if solve_example:
    for p in range(1, part + 1):
        solver.solve_examples(p, example_solutions[p - 1])
else:
    solver.solve_task(part, verbose=True)
