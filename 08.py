"""
--- Day 8: Haunted Wasteland ---

https://adventofcode.com/2023/day/8
"""

from __future__ import annotations

import math
import re
from pprint import pprint  # noqa: F401

from wrapper import Wrapper


class Node:
    nodes: dict[str, Node] = {}

    def __init__(self, definition: str) -> None:
        self._value, self._left_str, self._right_str = re.findall(r"[0-9A-Z]+", definition)
        self.nodes[self.value] = self

    @property
    def value(self) -> str:
        return self._value

    @property
    def left(self) -> Node:
        return self.nodes[self._left_str]

    @property
    def right(self) -> Node:
        return self.nodes[self._right_str]

    def __repr__(self) -> str:
        return f"""Node("{self.value} = ({self._left_str}, {self._right_str})")"""

    def __eq__(self, other: Node) -> bool:
        return self.value == other.value


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom

    def parse_custom(self, path) -> tuple[str, list[Node]]:
        nodes = []
        with open(path) as f:
            directions = f.readline().strip()
            f.readline()  # skip blank line
            for line in f:
                nodes.append(Node(line))
        return directions, nodes

    def task_1(self):
        directions, nodes = self.input
        start_list = [node for node in nodes if node.value == "AAA"]
        if not start_list:
            return 0
        steps = 0
        node = start_list[0]
        while node.value != "ZZZ":
            next_direction = directions[steps % len(directions)]
            if next_direction == "L":
                node = node.left
            else:
                node = node.right
            steps += 1
        return steps

    def task_2(self):
        directions: str = self.input[0]
        network: list[Node] = self.input[1]
        starts = {node.value: node for node in network if node.value.endswith("A")}
        print(f"{len(starts)=}")
        steps = 0
        nodes = starts
        shortest_route = {value: 0 for value in starts}
        while not all(shortest_route.values()):
            next_direction = directions[steps % len(directions)]
            steps += 1
            # pprint(nodes)
            # print(f"{next_direction=} {steps=}")
            if next_direction == "L":
                nodes = {start: node.left for start, node in nodes.items()}
            else:
                nodes = {start: node.right for start, node in nodes.items()}
            if steps % 1_000_000 == 0:
                print(f"{steps=:_d}")
            for start, node in nodes.copy().items():
                if node.value.endswith("Z"):
                    shortest_route[start] = steps
                    nodes.pop(start)
                    print(f"{shortest_route=}")
        return math.lcm(*shortest_route.values())


part = 2
solve_example = True
solve_example = False
example_solutions = [(2, 6, 0), (2, 6, 6)]

solver = Solver(day=8, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2, verbose=True)
