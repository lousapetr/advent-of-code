import re
from typing import Dict, List, Optional, Set, Tuple  # noqa: F401

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

    def simple_step(self, position: Tuple[int, int]) -> Tuple[Tuple[int, int], str]:
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
        return (new_row, new_col), trace

    def make_step_single(self, position: Tuple[int, int]) -> Tuple[int, int]:
        new_position, trace = self.simple_step(position)
        new_position = self.wrap_position(*new_position)
        new_row, new_col = new_position
        new_tile = self.board[new_row][new_col]
        if new_tile == "#":
            if (
                self.board[position[0]][position[1]] == " "
            ):  # if wall is hit, but currently in void, turn back and find last eligible
                self.direction = self.opposite_direction[self.direction]
                position = self.make_step_single(position)
                self.direction = self.opposite_direction[self.direction]
            return position
        elif new_tile == " ":
            return self.make_step_single(new_position)
        else:
            self.traced_board[new_row][new_col] = trace
            return new_position

    def wrap_position(self, row, col) -> Tuple[int, int]:
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

    def password(self, position: Optional[Tuple[int, int]] = None) -> int:
        if position is None:
            position = self.position
        direction_values = {d: val for val, d in enumerate("ESWN")}
        row = position[0] + 1
        col = position[1] + 1
        # print(self.direction)
        return 1000 * row + 4 * col + direction_values[self.direction]  # type: ignore


class JungleCube(Jungle):
    SIDE_LEN = 50
    SIDE_COORDS = [(0, 1), (0, 2), (1, 1), (2, 0), (2, 1), (3, 0)]

    def __init__(self, board: List[str], instructions) -> None:
        super().__init__(board, instructions)
        self.board = self.parse_board(board)
        self.position = (0, 0, 0)  # side, row, col

    def parse_board(self, board: List[str]) -> List[List[str]]:
        board_deck = []
        for side in range(6):
            side_row, side_col = self.SIDE_COORDS[side]
            row_range = board[side_row * self.SIDE_LEN : (side_row + 1) * self.SIDE_LEN]
            chars = [r[side_col * self.SIDE_LEN : (side_col + 1) * self.SIDE_LEN] for r in row_range]
            board_deck.append(chars)
        return board_deck

    def make_step_single(self, position: Tuple[int, int, int]) -> Tuple[int, int, int]:
        side = position[0]
        new_position, trace = self.simple_step(position[1:3])
        self.write_trace(trace, *position)
        row, col = new_position
        if (0 <= row < self.SIDE_LEN) and (0 <= col < self.SIDE_LEN):
            direction = self.direction
        else:
            side, row, col, direction = self.wrap_position(side, row, col)
        if self.board[side][row][col] != "#":
            self.direction = direction
            return side, row, col
        else:
            return position

    def wrap_position(self, side: int, row: int, col: int) -> Tuple[int, int, int, str]:
        """Returns (side_number, row, col, new_direction)"""
        last = self.SIDE_LEN - 1
        antirow = last - row
        match side:
            case 0:
                match self.direction:
                    case "N":
                        return (5, col, 0, "E")
                    case "E":
                        return (1, row, 0, "E")
                    case "S":
                        return (2, 0, col, "S")
                    case "W":
                        return (3, antirow, 0, "E")
            case 1:
                match self.direction:
                    case "N":
                        return (5, last, col, "N")
                    case "E":
                        return (4, antirow, last, "W")
                    case "S":
                        return (2, col, last, "W")
                    case "W":
                        return (0, row, last, "W")
            case 2:
                match self.direction:
                    case "N":
                        return (0, last, col, "N")
                    case "E":
                        return (1, last, row, "N")
                    case "S":
                        return (4, 0, col, "S")
                    case "W":
                        return (3, 0, row, "S")
            case 3:
                match self.direction:
                    case "N":
                        return (2, col, 0, "E")
                    case "E":
                        return (4, row, 0, "E")
                    case "S":
                        return (5, 0, col, "S")
                    case "W":
                        return (0, antirow, 0, "E")
            case 4:
                match self.direction:
                    case "N":
                        return (2, last, col, "N")
                    case "E":
                        return (1, antirow, last, "W")
                    case "S":
                        return (5, col, last, "W")
                    case "W":
                        return (3, row, last, "W")
            case 5:
                match self.direction:
                    case "N":
                        return (3, last, col, "N")
                    case "E":
                        return (4, last, row, "N")
                    case "S":
                        return (1, 0, col, "S")
                    case "W":
                        return (0, 0, row, "S")
        raise ValueError(f"Unexpected combination of {side=} and {self.direction=}")

    def get_original_coords(self, side: int, row: int, col: int) -> Tuple[int, int]:
        new_row = 50 * self.SIDE_COORDS[side][0] + row
        new_col = 50 * self.SIDE_COORDS[side][1] + col
        return new_row, new_col

    def write_trace(self, trace: str, side: int, row: int, col: int):
        tr_row, tr_col = self.get_original_coords(side, row, col)
        self.traced_board[tr_row][tr_col] = trace

    def password(self) -> int:
        position = self.get_original_coords(*self.position)
        return super().password(position)


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
        board, instructions = self.input
        jungle = JungleCube(board, instructions)
        jungle.travel()
        return jungle.password()


part = 2
solve_example = True
solve_example = False
example_solutions = [6032, 5031]

solver = Solver(day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1, verbose=False)
if part > 1:
    solver.solve_task(2, verbose=True)
