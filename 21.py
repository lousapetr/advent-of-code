from __future__ import annotations

import operator
from typing import Any, Callable, Dict, List, Set, Tuple, Union  # noqa: F401

from wrapper import Wrapper

# --- Day 21: Monkey Math ---
# https://adventofcode.com/2022/day/21

DAY_NUMBER = 21


class Monkey:
    monkey_instances: Dict[str, Monkey] = dict()

    def __init__(self, name: str, assignment: str):
        self.name = name
        self.monkey_instances[name] = self
        self._assignment = assignment

    @classmethod
    def reset(cls):
        for m in cls.monkey_instances.values():
            m.set_children()

    def set_children(self):
        try:
            self._value = int(self._assignment)
        except ValueError:
            self._value = None
            self.operation, self.children = self._parse_assignment(self._assignment)

    def _parse_assignment(self, assignment: str) -> Tuple[Callable, Tuple[Monkey, Monkey]]:
        monkey_1, op, monkey_2 = assignment.split()
        children = (self.monkey_instances[monkey_1], self.monkey_instances[monkey_2])
        if op == "+":
            operation = operator.add
        elif op == "-":
            operation = operator.sub
        elif op == "*":
            operation = operator.mul
        elif op == "/":
            operation = operator.truediv
        else:
            raise ValueError(f"Invalid operation {op}")
        return operation, children

    @property
    def value(self) -> Any:
        if self._value is None:
            self._value = self.operation(*[m.value for m in self.children])
        return self._value

    @value.setter
    def value(self, value: Union[int, complex]):
        self._value = value


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom

    def parse_custom(self, path) -> Dict[str, str]:
        list_input = self.parse_to_list(path)
        dict_input = dict()
        for line in list_input:
            key, value = line.split(": ", maxsplit=1)
            dict_input[key] = value
        return dict_input

    def task_1(self):
        for monkey, assignment in self.input.items():
            Monkey(monkey, assignment)
        Monkey.reset()
        return int(Monkey.monkey_instances["root"].value)

    def task_2(self):
        for monkey, assignment in self.input.items():
            Monkey(monkey, assignment)
        Monkey.reset()

        Monkey.monkey_instances["humn"].value = 0 + 1j  # use complex value as a polynom `0 + x`
        Monkey.monkey_instances["root"].operation = lambda x, y: (x, y)  # evaluate both branches separately

        # human side yields a polynom `real + imag * x`, monkey-only side yields number, solve equation for x
        human, desired = sorted(Monkey.monkey_instances["root"].value, key=lambda x: str(type))
        return int((desired - human.real) / human.imag)


part = 2
solve_example = True
solve_example = False
example_solutions = [152, 301]

solver = Solver(day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
