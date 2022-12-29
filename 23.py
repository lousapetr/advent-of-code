from __future__ import annotations

import curses
from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple  # noqa: F401

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

    def round(self, proposal_directions: str) -> List[ElfPosition]:
        elf_positions = set(self.elf_positions)
        move_proposals = [self.propose_move(elf, elf_positions, proposal_directions) for elf in self.elf_positions]
        proposal_counter = Counter(move_proposals)
        new_elf_positions = []
        for i, move in enumerate(move_proposals):
            if proposal_counter[move] == 1:
                new_elf_positions.append(move)
            else:
                new_elf_positions.append(self.elf_positions[i])
        return new_elf_positions

    def spread(self, n_rounds: int):
        proposal_directions = "NSWE"
        if self.verbose:
            self.show_elves()
        for i in range(n_rounds):
            self.elf_positions = self.round(proposal_directions)
            proposal_directions = proposal_directions[1:] + proposal_directions[0]
            if self.verbose:
                self.show_elves(round=(i + 1))

    def empty_ground(self) -> int:
        min_row = min(elf.row for elf in self.elf_positions)
        max_row = max(elf.row for elf in self.elf_positions)
        min_col = min(elf.col for elf in self.elf_positions)
        max_col = max(elf.col for elf in self.elf_positions)
        area = (max_row - min_row + 1) * (max_col - min_col + 1)
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
        for y in range(1, max_row + 5):
            for x in range(1, max_col + 5):
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
        self.verbose = self.example
        self.spread(n_rounds=10)
        return self.empty_ground()

    def task_2(self):
        self.elf_positions = self.input
        return NotImplemented


part = 1
solve_example = True
solve_example = False
example_solutions = [110, None]

solver = Solver(day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
