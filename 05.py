from wrapper import Wrapper
from typing import List, Tuple, Set, Dict  # noqa: F401

# https://adventofcode.com/2022/day/5

DAY_NUMBER = 5


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom
        self.input = super().load_input()
        self.cargo, self.moves = self.input

    def parse_cargo_lines(self, cargo_lines: List[str]) -> List[List[str]]:
        crate_lines = [line[1::4] for line in cargo_lines]
        cargo = [[""]] + [[] for _ in range(len(crate_lines[-1]))]
        for line in crate_lines:
            for i, crate in enumerate(line, start=1):
                if crate != " ":
                    cargo[i].insert(0, crate)
        return cargo

    def parse_moves_lines(self, moves_lines: List[str]) -> List[Dict[str, int]]:
        moves = []
        for line in moves_lines:
            _, move, _, src, _, dest = line.split()
            moves.append({"count": int(move), "from": int(src), "to": int(dest)})
        return moves

    def parse_custom(self, path):
        cargo_lines = []
        moves_lines = []
        with open(path) as f:
            for line in f:
                line = line.strip("\n")
                if not line:
                    continue
                if line.replace(" ", "").startswith("["):
                    cargo_lines.append(line)
                if line.startswith("move"):
                    moves_lines.append(line)
        cargo_parsed = self.parse_cargo_lines(cargo_lines)
        moves_parsed = self.parse_moves_lines(moves_lines)
        return cargo_parsed, moves_parsed

    def move_crates(self, move: Dict[str, int]):
        for _ in range(move["count"]):
            crate = self.cargo[move["from"]].pop()
            self.cargo[move["to"]].append(crate)

    def get_top_crates(self) -> str:
        top_crates = [stack[-1] for stack in self.cargo]
        return "".join(top_crates)

    def task_1(self):
        for move in self.moves:
            # print(move)
            self.move_crates(move)
            # print(self.cargo)
        # print(self.cargo)
        return self.get_top_crates()

    def task_2(self):
        return NotImplemented


part = 1
solve_example = True
solve_example = False
example_solutions = ["CMZ", None]

solver = Solver(
    day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions
)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
