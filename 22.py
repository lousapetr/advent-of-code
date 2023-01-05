import re
from typing import Dict, List, Set, Tuple  # noqa: F401

from wrapper import Wrapper

# --- Day 22: Monkey Map ---
# https://adventofcode.com/2022/day/22

DAY_NUMBER = 22


class Jungle:
    direction_changes = {"R": {"N": "E", "E": "S", "S": "W", "W": "N"}, "L": {"N": "W", "W": "S", "S": "E", "E": "N"}}
    opposite_direction = {"N": "S", "S": "N", "W": "E", "E": "W"}

    def __init__(self, board: List[str], instructions) -> None:
        self.board = board
        self.traced_board = [list(row) for row in self.board]
        self.instructions = instructions
        self.position = (0, board[0].index("."))  # row, col
        self.direction = "E"  # initially heading to right = EAST

    def __str__(self) -> str:
        # return "\n".join(self.board)
        return "\n".join(["".join(row) for row in self.traced_board])

    def travel(self):
        for x in self.instructions:
            if type(x) == int:
                self.position = self.make_steps(x)
            else:
                self.direction = self.direction_changes[x][self.direction]

    def make_steps(self, n_steps: int) -> Tuple[int, int]:
        new_position = self.position
        for step in range(n_steps):
            new_position = self.make_step_single(new_position)
        return new_position

    def make_step_single(self, position: Tuple[int, int]) -> Tuple[int, int]:
        row, col = position
        new_row, new_col = row, col
        trace = "X"
        match self.direction:
            case "N":
                new_row = row - 1
                trace = "^"
            case "S":
                new_row = row + 1
                trace = "v"
            case "W":
                new_col = col - 1
                trace = "<"
            case "E":
                new_col = col + 1
                trace = ">"

        new_row, new_col = self.normalize_position(new_row, new_col)
        new_position = (new_row, new_col)
        new_tile = self.board[new_row][new_col]
        if new_tile == "#":
            if self.board[row][col] == " ":  # if wall is hit, but currently in void, turn back and find last eligible
                self.direction = self.opposite_direction[self.direction]
                position = self.make_step_single(position)
                self.direction = self.opposite_direction[self.direction]
            return position
        elif new_tile == " ":
            return self.make_step_single(new_position)
        else:
            self.traced_board[new_row][new_col] = trace
            return new_position

    def normalize_position(self, row, col) -> Tuple[int, int]:
        row_count = len(self.board)
        col_count = len(self.board[0])
        if row < 0:
            row += row_count
        elif row >= row_count:
            row -= row_count
        if col < 0:
            col += col_count
        elif col >= col_count:
            col -= col_count
        return row, col

    def password(self) -> int:
        direction_values = {d: val for val, d in enumerate("ESWN")}
        row = self.position[0] + 1
        col = self.position[1] + 1
        # print(self.direction)
        return 1000 * row + 4 * col + direction_values[self.direction]  # type: ignore


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom

    def parse_custom(self, path):
        board = []
        instructions = ""
        with open(path) as f:
            for line in f:
                line = line.strip("\n")
                if line:
                    board.append(line)
                else:
                    instructions = next(f).strip()
        max_length = max(len(row) for row in board)
        board = [row + " " * (max_length - len(row)) for row in board]
        instructions = [int(x) if x.isnumeric() else x for x in re.findall("([0-9]+|[RL])", instructions)]
        return board, instructions

    def task_1(self):
        board, instructions = self.input
        jungle = Jungle(board, instructions)
        # print(jungle)
        print()
        jungle.travel()
        print(jungle)
        return jungle.password()

    def task_2(self):
        return NotImplemented


part = 1
solve_example = True
solve_example = False
example_solutions = [6032, None]

solver = Solver(day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1, verbose=True)
if part > 1:
    solver.solve_task(2)
