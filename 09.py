from wrapper import Wrapper
from typing import List, Tuple, Set, Dict  # noqa: F401
import numpy as np
from numpy.typing import NDArray

# https://adventofcode.com/2022/day/9

DAY_NUMBER = 9


class Rope:
    def __init__(self, tail_length: int = 1) -> None:
        self._head = np.zeros(2, dtype=int)  # x, y
        self._tail = np.zeros((tail_length, 2), dtype=int)
        self._tail_visited: Set[Tuple[int, int]] = {(0, 0)}

    def move(self, motion: str):
        parsed_motion = self.parse_motion(motion)
        # print(parsed_motion)
        for move in parsed_motion:
            # print(f"{move=}")
            self._move_head(move)
            # print(f"{self._head=}")
            self._move_tail()
            # print(f"{self._tail=}")

    def visited_count(self) -> int:
        return len(self._tail_visited)

    @staticmethod
    def parse_motion(motion: str) -> List[np.ndarray]:
        direction, count = motion.strip().split()
        count = int(count)
        move_map = {"R": [1, 0], "L": [-1, 0], "U": [0, 1], "D": [0, -1]}
        return [np.array(move_map[direction]) for _ in range(count)]

    def _move_head(self, move: np.ndarray) -> None:
        self._head += move

    def _move_knot(self, head: NDArray[np.int_], knot: NDArray[np.int_]) -> np.ndarray:
        tail_lag = head - knot
        if np.max(np.abs(tail_lag)) <= 1:  # touching at least diagonally
            pass
        else:
            knot += np.sign(tail_lag)  # move one step toward head
        return knot

    def _move_tail(self) -> None:
        for i, knot in enumerate(self._tail):
            if i == 0:
                head = self._head
            else:
                head = self._tail[i - 1]
            self._tail[i] = self._move_knot(head, knot)
        self._tail_visited.add(tuple(self._tail[-1]))

    def __str__(self) -> str:
        # size = sum(self._tail_visited, start=())
        # return str(size)
        return str(self._tail)


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_to_list

    def task(self, tail_length: int) -> int:
        rope = Rope(tail_length=tail_length)
        for motion in self.input:
            rope.move(motion)
            # print(rope)
        return rope.visited_count()

    def task_1(self):
        return self.task(tail_length=1)

    def task_2(self):
        return self.task(tail_length=9)


part = 2
solve_example = True
# solve_example = False
example_solutions = [13, (1, 36)]

solver = Solver(day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
