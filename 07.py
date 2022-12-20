from __future__ import annotations
from wrapper import Wrapper
from typing import List, Tuple, Set, Dict, Union, Optional  # noqa: F401
from abc import ABC, abstractproperty

# https://adventofcode.com/2022/day/7

DAY_NUMBER = 7


class Node(ABC):
    def __init__(self, name: str) -> None:
        self._size = None
        self._name = name
        self._parent = None

    @abstractproperty
    def size(self):
        pass

    @property
    def parent(self) -> Directory:
        if self._parent:
            return self._parent
        else:
            return Directory("None")

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self._name}")'


class File(Node):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, value: int):
        self._size = value

    @property
    def parent(self) -> Directory:
        return super().parent

    @parent.setter
    def parent(self, parent: Directory):
        self._parent = parent
        parent.add_child(self)


class Directory(Node):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self._parent = None
        self.children: List[Union[File, Directory]] = []

    @property
    def size(self) -> int:
        if self._size:
            return self._size
        return sum(child.size for child in self.children)

    @property
    def parent(self) -> Directory:
        return super().parent

    @parent.setter
    def parent(self, parent: Directory):
        self._parent = parent
        parent.add_child(self)

    def add_child(self, child: Union[Directory, File]):
        self.children.append(child)


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_custom

    def parse_custom(self, path):
        root = Directory("root")
        current_dir = root
        all_directories = [root]
        with open(path) as f:
            for line in f:
                line = line.strip().split()
                if line[0] == "$":  # command
                    if line[1] == "ls":
                        continue
                    if line[1] == "cd":
                        if line[2] == "..":
                            current_dir = current_dir.parent
                            continue
                        else:
                            new_dir = Directory(line[2])
                            new_dir.parent = current_dir
                            current_dir = new_dir
                            all_directories.append(new_dir)
                            continue
                elif line[0] == "dir":
                    continue
                else:
                    new_file = File(line[-1])
                    new_file.size = int(line[0])
                    new_file.parent = current_dir
        return all_directories

    def task_1(self):
        sizes = [d.size for d in self.input]
        small_dirs = filter(lambda x: x < 100_000, sizes)
        # file_sizes = [
        #     [(child._name, child.size) for child in d.children] for d in self.input
        # ]
        # print(file_sizes)
        return sum(small_dirs)

    def task_2(self):
        sizes = [d.size for d in self.input]
        total_disk = 70_000_000
        required_space = 30_000_000
        root_size = [d.size for d in self.input if d._name == "/"][0]
        currently_free_space = total_disk - root_size
        to_delete = required_space - currently_free_space
        # print(f"{root_size=}")
        # print(f"{currently_free_space=}")
        # print(f"{to_delete=}")
        big_enough = [s for s in sizes if s >= to_delete]
        return min(big_enough)


part = 2
solve_example = True
solve_example = False
example_solutions = [95437, 24933642]

solver = Solver(day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)
