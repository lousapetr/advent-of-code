from __future__ import annotations

import curses
from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple  # noqa: F401

import pandas as pd

from wrapper import Wrapper

# --- Day 23: Unstable Diffusion ---
# https://adventofcode.com/2022/day/23

DAY_NUMBER = 23


@dataclass
class ElfPosition:
    row: int
    col: int

    def __hash__(self) -> int:
        return hash((self.row, self.col))

    def north(self) -> ElfPosition:
        return ElfPosition(row=(self.row - 1), col=self.col)

    def south(self) -> ElfPosition:
        return ElfPosition(row=(self.row + 1), col=self.col)

    def west(self) -> ElfPosition:
        return ElfPosition(row=self.row, col=(self.col - 1))

    def east(self) -> ElfPosition:
        return ElfPosition(row=self.row, col=(self.col + 1))

    def north_neigbours(self) -> Set[ElfPosition]:
        return {ElfPosition(row=(self.row - 1), col=(self.col + i)) for i in [-1, 0, 1]}

    def south_neigbours(self) -> Set[ElfPosition]:
        return {ElfPosition(row=(self.row + 1), col=(self.col + i)) for i in [-1, 0, 1]}

    def west_neigbours(self) -> Set[ElfPosition]:
        return {ElfPosition(row=(self.row + i), col=(self.col - 1)) for i in [-1, 0, 1]}

    def east_neigbours(self) -> Set[ElfPosition]:
        return {ElfPosition(row=(self.row + i), col=(self.col + 1)) for i in [-1, 0, 1]}

    def all_neighbours(self) -> Set[ElfPosition]:
        return {ElfPosition(row=(self.row + i), col=(self.col + j)) for i in [-1, 0, 1] for j in [-1, 0, 1]} - {self}


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom
        self.elf_positions: List[ElfPosition]
        self.history: List[Dict[str, int]] = []

    def parse_custom(self, path) -> List[ElfPosition]:
        lines = self.parse_to_list(path, comment="-")
        elf_positions = []
        for i, line in enumerate(lines):
            for j, char in enumerate(line):
                if char == "#":
                    elf_positions.append(ElfPosition(row=i, col=j))  # row, col
        return elf_positions

    def propose_move(self, elf: ElfPosition, elf_positions: Set[ElfPosition], proposal_directions: str) -> ElfPosition:
        directions = {
            "N": (elf.north_neigbours(), elf.north()),
            "S": (elf.south_neigbours(), elf.south()),
            "W": (elf.west_neigbours(), elf.west()),
            "E": (elf.east_neigbours(), elf.east()),
        }
        if not elf.all_neighbours().intersection(elf_positions):  # don't move if alone
            return elf
        for hood, move in [directions[d] for d in proposal_directions]:
            if not hood.intersection(elf_positions):
                return move
        return elf  # if all directions are occupied

    def round(self, proposal_directions: str) -> Tuple[List[ElfPosition], int]:
        elf_positions = set(self.elf_positions)
        move_proposals = [self.propose_move(elf, elf_positions, proposal_directions) for elf in self.elf_positions]
        proposal_counter = Counter(move_proposals)
        new_elf_positions = []
        moved_count = 0
        for orig_pos, move in zip(self.elf_positions, move_proposals):
            if proposal_counter[move] == 1 and move != orig_pos:
                new_elf_positions.append(move)
                moved_count += 1
            else:
                new_elf_positions.append(orig_pos)
        return new_elf_positions, moved_count

    def spread(self, n_rounds: Optional[int]):
        proposal_directions = "NSWE"
        if self.verbose:
            self.show_elves()
        round_count = 0
        self.history += [
            {"round": round_count, "x": elf.col, "y": elf.row, "id": i} for i, elf in enumerate(self.elf_positions)
        ]
        while True:
            round_count += 1
            if n_rounds and round_count > n_rounds:
                return self.empty_ground()
            new_positions, moved_count = self.round(proposal_directions)
            print(f"Round {round_count:3d}\t Moved elves: {moved_count:4d}", end="\t")
            self.empty_ground()
            self.history += [
                {"round": round_count, "x": elf.col, "y": elf.row, "id": i} for i, elf in enumerate(new_positions)
            ]
            if new_positions != self.elf_positions:
                self.elf_positions = new_positions
            else:
                return round_count
            proposal_directions = proposal_directions[1:] + proposal_directions[0]
            if self.verbose:
                self.show_elves(round=(round_count + 1))

    def empty_ground(self) -> int:
        min_row = min(elf.row for elf in self.elf_positions)
        max_row = max(elf.row for elf in self.elf_positions)
        min_col = min(elf.col for elf in self.elf_positions)
        max_col = max(elf.col for elf in self.elf_positions)
        area = (max_row - min_row + 1) * (max_col - min_col + 1)
        print(f"Covered area: rows ({min_row:4d}, {max_row:4d}), cols ({min_col:4d}, {max_col:4d})")
        return area - len(self.elf_positions)

    @staticmethod
    def _show_elves_curses(stdscr: curses._CursesWindow, elf_positions: List[ElfPosition], round: int):
        min_row = min(min(elf.row for elf in elf_positions), -10)
        max_row = max(max(elf.row for elf in elf_positions), 30)
        min_col = min(min(elf.col for elf in elf_positions), -10)
        max_col = max(max(elf.col for elf in elf_positions), 30)
        stdscr.clear()
        if round == 0:
            stdscr.addstr(0, 0, "== Initial state ==")
        else:
            stdscr.addstr(0, 0, f"== End of Round {round} ==")
        for y in range(1, max_row - min_row + 5):
            for x in range(1, max_col - min_col + 5):
                elf_x, elf_y = x + min_col, y + min_row
                if ElfPosition(row=elf_y, col=elf_x) in elf_positions:
                    stdscr.addch(y, x, "#")
                else:
                    stdscr.addch(y, x, ".")

        stdscr.refresh()
        # stdscr.getkey()
        if stdscr.getch() == ord("q"):
            quit()

    def show_elves(self, round: int = 0):
        curses.wrapper(self._show_elves_curses, self.elf_positions, round=round)

    def task_1(self):
        self.elf_positions = self.input
        # self.verbose = self.example
        self.verbose = False
        result = self.spread(n_rounds=10)
        return result

    def task_2(self):
        self.elf_positions = self.input
        # self.verbose = self.example
        self.verbose = False
        result = self.spread(n_rounds=None)
        output_path = "inputs/23_output_example.csv" if self.example else "inputs/23_output.csv"
        history_df = pd.DataFrame.from_records(self.history)
        history_df.to_csv(output_path)
        return result


part = 2
solve_example = True
solve_example = False
example_solutions = [110, 20]

solver = Solver(day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2, verbose=True)
