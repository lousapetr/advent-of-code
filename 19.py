"""
--- Day 19: Aplenty ---

https://adventofcode.com/2023/day/19
"""

from pprint import pprint  # noqa: F401

from wrapper import Wrapper


class Part:
    def __init__(self, description: str) -> None:
        self.properties = {}
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

    def __str__(self) -> str:
        return f"{self.name:3s} = {self.rules}"


class Workshop:
    def __init__(self, input: str) -> None:
        self.workflows: dict[str, Workflow]
        self.parts: list[Part]
        self.workflows, self.parts = self.parse_input(input)

    def process_all_parts(self) -> None:
        for part in self.parts:
            self.process_part(part)

    def process_part(self, part: Part) -> None:
        workflow_name = "in"
        while workflow_name not in "AR":
            workflow = self.workflows[workflow_name]
            workflow_name = workflow.apply_rules(part)
        part.status = workflow_name

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

    def parse_custom(self, path) -> Workshop:
        with open(path) as f:
            return Workshop(f.read())

    def task_1(self):
        workshop: Workshop = self.input
        workshop.process_all_parts()
        return workshop.total_rating

    def task_2(self):
        return NotImplemented


part = 1
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
