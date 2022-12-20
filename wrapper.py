import pandas as pd
import numpy as np
from typing import Sequence, List, Any, Callable, Optional, Union, Tuple
import sys
import os
import time
import pprint
from abc import ABC, abstractmethod


class HiddenPrints:
    """Helper class for suppressing printing"""

    # https://stackoverflow.com/a/45669280/9003767
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


class Wrapper(ABC):
    def __init__(
        self,
        day: int,
        example: bool,
        example_solutions: Sequence[Union[int, str, Sequence[Union[int, str]]]],
    ):
        """
        Parameters
        ----------
        day : int
            number of current day - used for setting paths to inputs
        example : bool
            True if using example input
            False if using real task input
        example_solutions:
            - 2-element list containing correct solutions for example of Part 1 and Part 2
            - initially (before solving Part 1), second element is None
            - if there are multiple example inputs, each element might be a list or tuple
        """
        self.day = day
        self.example = example
        self.example_solutions = example_solutions
        self.input_path = f"./inputs/{self.day:02d}_input.txt"
        self.example_path_template = f"./inputs/{self.day:02d}_input_example{{}}.txt"
        self.input: Any = None
        self.parser: Callable = self.parse_custom
        self.parser_kwargs = None

    def load_input(self, path: str) -> None:
        """
        Loads input using specified parser and saves it into an internal variable.
        """
        if self.parser_kwargs:
            self.input = self.parser(path, **self.parser_kwargs)
        else:
            self.input = self.parser(path)

    def print_input(self):
        """Pretty print the parsed input"""
        print("=" * 15)
        print("Input:")
        pprint.pprint(self.input)
        print()

    def parse_to_list(self, path: str, comment: str = "#") -> List[str]:
        """Parse input file to list of lines

        Parameters
        ----------
        path : str
            path to input file
        comment : str, optional
            ignore lines starting by this character, by default '#'

        Returns
        -------
        List[str]
            list of lines as strings
        """
        with open(path) as f:
            lines = f.readlines()
            return [line.strip() for line in lines if not line.startswith(comment)]

    def parse_to_pandas_df(self, path: str, **kwargs) -> pd.DataFrame:
        """Parse input file to pandas dataframe, can specify delimiter, header, names, dtype or other

        Parameters
        ----------
        path : str
            path to input file

        Returns
        -------
        pd.DataFrame
            dataframe interpreting the input file as CSV
        """
        kwargs.setdefault("delimiter", " ")
        kwargs.setdefault("header", None)
        kwargs.setdefault("names", None)
        kwargs.setdefault("dtype", int)
        text_reader = pd.read_csv(path, **kwargs)
        df = pd.concat(text_reader, ignore_index=True)
        return df

    def parse_to_array(self, path: str) -> np.ndarray:
        """Parse input file to numpy array, ignoring lines starting by `#`

        Parameters
        ----------
        path : str
            path to input file

        Returns
        -------
        np.ndarray[int]
            numpy array of integers
        """
        line_list = self.parse_to_list(path)
        matrix = [[int(i) for i in x] for x in line_list if x[0] != "#"]
        return np.array(matrix)

    def parse_custom(self):
        pass

    def array_to_string(self, matrix: np.ndarray, format: str = "1d", delimiter: str = "") -> str:
        """
        Create string representation of numpy matrix
        """
        return "\n".join(f"{delimiter}".join(f"{num:{format}}" for num in row) for row in matrix)

    def solve_task(self, task_number: int, verbose: Optional[bool] = None, time_fmt: str = ",.1f"):
        """Wrapper for solving tasks

        - selects appropriate function to run
        - measures elapsed time
        - can suppress all prints from the running code
        - checks if the solution of the examples is correct

        Parameters
        ----------
        task_number : int, 1 or 2
            number of part to solve
        verbose : bool, optional
            if False, suppress all prints
            if True, allow printing
            by default None - True if self.example is True, False otherwise
        time_fmt : str, optional
            format for printing elapsed time, by default ',.1f'
        """
        print("=" * 15)
        print(f"Task {task_number}")
        if verbose is None:
            verbose = self.example  # be verbose if solving example

        if task_number == 1:
            task_func = self.task_1
        elif task_number == 2:
            task_func = self.task_2
        else:
            raise ValueError(f"Incorrect task number - {task_number}. Must equal to 1 or 2.")

        if self.example:
            self.solve_examples(task_func, task_number, verbose)
        else:
            self.load_input(self.input_path)
            if verbose:
                self.print_input()
            result, run_time = self.run_task(task_func, verbose)
            print(f"Elapsed time: {run_time * 1000:{time_fmt}} ms")
            print("Result:", result)
        print("=" * 15)

    def run_task(self, task_func: Callable, verbose: bool) -> Tuple[Any, float]:
        """
        Wrapper method that runs a task and returns the result with elapsed time.

        :return: result of task, time spent with calculation
        :rtype: Tuple[Any, float]
        """
        if verbose:
            start_time = time.perf_counter()
            result = task_func()
            end_time = time.perf_counter()
        else:
            with HiddenPrints():  # suppress all prints
                start_time = time.perf_counter()
                result = task_func()
                end_time = time.perf_counter()
        return result, end_time - start_time

    def solve_examples(self, task_func: Callable, task_number: int, verbose: bool):
        """
        Solve for example inputs and compares to expected results.
        Allows multiple input files.
        """
        solution = self.example_solutions[task_number - 1]
        if type(solution) in (int, str) or solution is None:
            solution = [solution]
        solution = list(solution)  # type: ignore
        path_extensions = [""] + [f"_{i}" for i in range(1, len(solution))]
        example_input_paths = [self.example_path_template.format(ext) for ext in path_extensions]
        for sol, path in zip(solution, example_input_paths):
            self.load_input(path)
            self.print_input()
            result, run_time = self.run_task(task_func, verbose)
            print(f"Elapsed time: {run_time * 1000:,.1f} ms")
            if result != sol:
                print("Incorrect solution!")
                print(f"Should get:  {sol}")
                print(f"Got instead: {result}")
            else:
                print("Correct solution!")
                print("Result:", result)

    @abstractmethod
    def task_1(self) -> Union[int, str]:
        pass

    @abstractmethod
    def task_2(self) -> Union[int, str]:
        pass
