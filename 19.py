"""
--- Day 19: Aplenty ---

https://adventofcode.com/2023/day/19
"""

from __future__ import annotations

from copy import deepcopy
from math import prod
from operator import gt, lt
from pprint import pprint  # noqa: F401
from typing import Callable, Iterable

from wrapper import Wrapper


class Part:
    def __init__(self, description: str) -> None:
        self.properties: dict[str, int] = {}
        for property in description.strip("{}").split(","):
            name, value_str = property.split("=")
            self.properties[name] = int(value_str)
        self.status: str = ""

    @property
    def rating(self) -> int:
        if self.status != "A":
            return 0
        return sum(self.properties.values())

    def __str__(self) -> str:
        properties = "{" + ", ".join(f"{p}: {value:4d}" for p, value in self.properties.items()) + "}"
        return f"{properties} => {self.status}"


class PartRange:
    def __init__(self) -> None:
        self.properties: dict[str, Iterable[int]] = {p: range(1, 4001) for p in "xmas"}

    def _compare(self, comparison_char: str, value: int, opposite: bool = False) -> Callable[[int], bool]:
        comparison_func = lt if comparison_char == "<" else gt

        def func(x: int) -> bool:
            condition = comparison_func(x, value)
            return condition ^ opposite  # XOR

        return func

    def split_by_rule(self, rule: str) -> tuple[PartRange, PartRange]:
        """
        Splits the range by the rule.

        Returns first the range that fits the rule, second the range that doesn't fit the rule.
        """
        new_pr = deepcopy(self)
        p, comparator, value = rule[0], rule[1], int(rule[2:])
        self.properties[p] = list(filter(self._compare(comparator, value), self.properties[p]))
        new_pr.properties[p] = list(filter(self._compare(comparator, value, opposite=True), new_pr.properties[p]))
        return self, new_pr

    @property
    def combination_count(self) -> int:
        return prod(len(list(r)) for r in self.properties.values())

    def __repr__(self) -> str:
        properties = ", ".join(
            f"{p}:{range(min(list(values)), max(list(values)) + 1)}" for p, values in self.properties.items()
        )
        return f"PartRange({properties})"


class Workflow:
    def __init__(self, description: str) -> None:
        self.name, rules_raw = description.strip("}").split("{")
        self.rules = rules_raw.split(",")

    def apply_rules(self, part: Part) -> str:
        for rule in self.rules:
            if ":" not in rule:  # default target
                return rule
            rule, result = rule.split(":")
            p, value = rule[0], int(rule[2:])
            if ("<" in rule and part.properties[p] < value) or (">" in rule and part.properties[p] > value):
                return result
        raise ValueError(f"WTF? '{part=}' '{self=}'")

    def apply_rules_to_ranges(self, ranges: list[PartRange], workflows: dict[str, Workflow]) -> list[PartRange]:
        acceptable_ranges: list[PartRange] = []
        for part_range in ranges:
            for rule in self.rules:
                if rule == "A":
                    acceptable_ranges.append(part_range)
                    continue
                if rule == "R":
                    continue
                if ":" not in rule:  # default workflow
                    acceptable_ranges += workflows[rule].apply_rules_to_ranges([part_range], workflows)
                    continue
                rule, target = rule.split(":")
                pr_pass, pr_fail = part_range.split_by_rule(rule)
                if target == "A":
                    acceptable_ranges.append(pr_pass)
                elif target == "R":
                    pass
                else:
                    acceptable_ranges += workflows[target].apply_rules_to_ranges([pr_pass], workflows)
                part_range = pr_fail
        return acceptable_ranges

    def __str__(self) -> str:
        return f"{self.name:3s} = {self.rules}"


class Workshop:
    def __init__(self, input: str) -> None:
        self.workflows: dict[str, Workflow]
        self.parts: list[Part]
        self.workflows, self.parts = self.parse_input(input)
        self.parts_ranges: list[PartRange]

    def process_all_parts(self) -> None:
        for part in self.parts:
            self.process_part(part)

    def process_part(self, part: Part) -> None:
        workflow_name = "in"
        while workflow_name not in "AR":
            workflow = self.workflows[workflow_name]
            workflow_name = workflow.apply_rules(part)
        part.status = workflow_name

    def find_acceptable_ranges(self) -> list[PartRange]:
        workflow = self.workflows["in"]
        return workflow.apply_rules_to_ranges([PartRange()], self.workflows)

    def parse_input(self, input: str) -> tuple[dict[str, Workflow], list[Part]]:
        workflows = {}
        parts = []
        workflows_block, parts_block = input.split("\n\n")
        for line in workflows_block.splitlines():
            wf = Workflow(line)
            workflows[wf.name] = wf
        for line in parts_block.splitlines():
            parts.append(Part(line))
        return workflows, parts

    @property
    def total_rating(self) -> int:
        return sum(p.rating for p in self.parts)

    def __repr__(self) -> str:
        return "\n".join(map(str, self.workflows.values())) + "\n" + "\n".join(map(str, self.parts))


class Solver(Wrapper):
    def __init__(self, **kwargs):
        self.parser = self.parse_custom
        super().__init__(**kwargs)
        self.input: Workshop

    def parse_custom(self, path) -> Workshop:
        with open(path) as f:
            return Workshop(f.read())

    def task_1(self):
        workshop = self.input
        workshop.process_all_parts()
        return workshop.total_rating

    def task_2(self):
        workshop = self.input
        acceptable_ranges = workshop.find_acceptable_ranges()
        return sum(pr.combination_count for pr in acceptable_ranges)


part = 2
solve_example = True
solve_example = False
example_solutions = [19114, 167409079868000]

solver = Solver(year=2023, day=19)
# solve always all examples, but only one final task
if solve_example:
    for p in range(1, part + 1):
        solver.solve_examples(p, example_solutions[p - 1])
else:
    solver.solve_task(part, verbose=False)
    solver.submit_answer(part)
