from __future__ import annotations
from wrapper import Wrapper
from typing import List, Tuple, Set, Dict, Callable  # noqa: F401
import re
from functools import partial

# https://adventofcode.com/2022/day/11

DAY_NUMBER = 11


class MonkeyTroop:
    def __init__(self, monkey_blocks: List[List[str]]) -> None:
        self.monkey_list = [Monkey(block) for block in monkey_blocks]
        self.monkeys = {monkey.number: monkey for monkey in self.monkey_list}

    def take_round(self):
        for monkey in self.monkey_list:
            monkey.take_turn(self.monkeys)

    def get_monkey_business(self) -> int:
        most_active_monkeys = sorted(
            (m.inspection_counter for m in self.monkey_list), reverse=True
        )
        return most_active_monkeys[0] * most_active_monkeys[1]


class Monkey:
    number_regex = re.compile(r"(\d+)")

    def __init__(self, monkey_block: List[str]) -> None:
        self.number = re.findall(self.number_regex, monkey_block[0])[0]
        self.items = [int(n) for n in re.findall(self.number_regex, monkey_block[1])]
        operation_line = monkey_block[2]
        self.inspect = self._operation(operation_line)
        self.test_divisor = int(re.findall(self.number_regex, monkey_block[3])[0])
        self.true = re.findall(self.number_regex, monkey_block[4])[0]
        self.false = re.findall(self.number_regex, monkey_block[5])[0]

        self.inspection_counter = 0

    def _operation(self, op_line: str) -> Callable:
        if "old + old" in op_line:
            return partial(self._multiplication, factor=2)
        if "old * old" in op_line:
            return partial(self._power, power=2)
        factor = int(re.findall(self.number_regex, op_line)[0])
        if "old +" in op_line:
            return partial(self._addition, factor=factor)
        if "old *" in op_line:
            return partial(self._multiplication, factor=factor)
        raise ValueError(f"Invalid operation line: {op_line=}")

    @staticmethod
    def _addition(old: int, factor: int) -> int:
        return old + factor

    @staticmethod
    def _multiplication(old: int, factor: int) -> int:
        return old * factor

    @staticmethod
    def _power(old: int, power: int) -> int:
        return old ** power

    def take_turn(self, monkey_dict: Dict[str, Monkey]):
        print(f"Monkey {self.number}:")
        print(f"    Start of turn items: {self.str_items()}")
        for item in self.items:
            worry_level = self.inspect(item)
            self.inspection_counter += 1
            worry_level //= 3
            if worry_level % self.test_divisor == 0:
                target = monkey_dict[self.true]
            else:
                target = monkey_dict[self.false]
            self.throw(worry_level, target)
        self.items = []

    @staticmethod
    def throw(worry_level: int, target: Monkey):
        print(f"    Throwing {worry_level} to Monkey {target.number}")
        target.receive(worry_level)

    def receive(self, worry_level: int):
        self.items.append(worry_level)

    def str_items(self):
        return ", ".join(str(n) for n in self.items)


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom

    def parse_custom(self, path) -> List[List[str]]:
        monkey_blocks = []
        single_monkey_lines = []
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line:
                    single_monkey_lines.append(line)
                else:
                    monkey_blocks.append(single_monkey_lines)
                    single_monkey_lines = []
            monkey_blocks.append(single_monkey_lines)
        return monkey_blocks

    def task_1(self):
        monkey_troop = MonkeyTroop(monkey_blocks=self.input)
        for _ in range(20):
            monkey_troop.take_round()
        for monkey in monkey_troop.monkey_list:
            print(
                f"Monkey {monkey.number} inspected items {monkey.inspection_counter:4d} times."
            )
        return monkey_troop.get_monkey_business()

    def task_2(self):
        return NotImplemented


part = 1
solve_example = True
solve_example = False
example_solutions = [10605, None]

solver = Solver(
    day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions
)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
