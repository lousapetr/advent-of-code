import os
import pprint
import sys
import time
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable, Optional, Sequence

import requests

if TYPE_CHECKING:
    import numpy as np
    import pandas as pd


class HiddenPrints:
    """Helper class for suppressing printing"""

    # https://stackoverflow.com/a/45669280/9003767
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

    @classmethod
    def bold(cls, string: Any) -> str:
        return f"{cls.BOLD}{string}{cls.ENDC}"

    @classmethod
    def fail(cls, string: Any) -> str:
        return f"{cls.BOLD}{cls.FAIL}{string}{cls.ENDC}"

    @classmethod
    def warning(cls, string: Any) -> str:
        return f"{cls.WARNING}{string}{cls.ENDC}"

    @classmethod
    def okblue(cls, string: Any) -> str:
        return f"{cls.OKBLUE}{string}{cls.ENDC}"

    @classmethod
    def okgreen(cls, string: Any) -> str:
        return f"{cls.BOLD}{cls.OKGREEN}{string}{cls.ENDC}"


class Wrapper(ABC):
    def __init__(
        self,
        year: int,
        day: int,
    ):
        """
        Parameters
        ----------
        year : int
            current year - used for setting paths and for final submission
        day : int
            number of current day - used for setting paths to inputs
        example : bool
            True if using example input
            False if using real task input
        """
        self.year = year
        self.day = day
        self.input_path = f"./inputs/{self.day:02d}_input.txt"
        self.example_path_template = f"./inputs/{self.day:02d}_input_example{{}}.txt"
        self.parser = self.parse_custom
        self.parser_kwargs = {}
        # TODO fix the parser type - try https://chat.openai.com/share/5f75c0e9-698a-408f-ad50-92b9a880fc98 (last part)
        self.input = self.parser(self.example_path_template.format(""), **self.parser_kwargs)
        self.result: int | str = "Not found yet"

    def load_input(self, path: str) -> None:
        """
        Loads input using specified parser and saves it into an internal variable.
        """
        self.input = self.parser(path, **self.parser_kwargs)

    def print_input(self):
        """Pretty print the parsed input"""
        print("=" * 15)
        print("Input:")
        pprint.pprint(self.input)
        print()

    def parse_to_list(self, path: str, astype: Callable = str, comment: str = "None") -> list[Any]:
        """Parse input file to list of lines

        Parameters
        ----------
        path : str
            path to input file
        astype: Callable
            convert each line by given function
        comment : str, optional
            ignore lines starting by this character, by default 'None'

        Returns
        -------
        List[Any]
            list of lines as strings or converted to another type
        """
        with open(path) as f:
            lines = [line.strip() for line in f.readlines() if not line.startswith(comment)]
        try:
            return [astype(line) for line in lines]
        except ValueError:
            return lines

    def parse_to_pandas_df(self, path: str, **kwargs) -> "pd.DataFrame":
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
        import pandas as pd

        kwargs.setdefault("delimiter", " ")
        kwargs.setdefault("header", None)
        kwargs.setdefault("names", None)
        kwargs.setdefault("dtype", int)
        text_reader = pd.read_csv(path, **kwargs)
        df = pd.concat(text_reader, ignore_index=True)
        return df

    def parse_to_array(self, path: str) -> "np.ndarray":
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
        import numpy as np

        line_list = self.parse_to_list(path)
        matrix = [[int(i) for i in x] for x in line_list if x[0] != "#"]
        return np.array(matrix)

    def parse_custom(self, path: str):
        pass

    @staticmethod
    def array_to_string(matrix: Sequence[Sequence[Any]], fmt: str = "1", delimiter: str = "") -> str:
        """
        Create string representation of a 2D array
        """
        return "\n".join(f"{delimiter}".join(f"{num:{fmt}}" for num in row) for row in matrix)

    def solve_task(self, task_number: int, verbose: bool = False, time_fmt: str = ",.1f") -> None:
        """Wrapper for solving tasks with full input

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
        time_fmt : str, optional
            format for printing elapsed time, by default ',.1f'
        """
        print("=" * 15)
        print(f"Task {task_number}")
        self.load_input(self.input_path)
        if verbose:
            self.print_input()
        self.result, run_time = self.run_task(task_number, verbose)
        print(f"Elapsed time: {run_time * 1000:{time_fmt}} ms")
        print(f"Result: {Colors.okblue(self.result)}")
        print("=" * 15)

    def run_task(self, task_number: int, verbose: bool) -> tuple[int | str, float]:
        """
        Wrapper method that runs a task and returns the result with elapsed time.

        :return: result of task, time spent with calculation
        """
        if task_number == 1:
            task_func = self.task_1
        elif task_number == 2:
            task_func = self.task_2
        else:
            raise ValueError(f"Incorrect task number - {task_number}. Must equal to 1 or 2.")

        start_time = time.perf_counter()
        if verbose:
            result = task_func()
        else:
            with HiddenPrints():  # suppress all prints
                result = task_func()
        end_time = time.perf_counter()
        return result, end_time - start_time

    def submit_answer(self, task_number: int) -> None:
        """
        Submit the final answer to the AoC webpage and evaluate the success.
        """
        # TODO submit the answer automatically using requests.post
        with open("./aoc_token.txt") as f:
            cookie = f.read().strip()
        base_url = f"https://adventofcode.com/{self.year}/day/{self.day}"
        r = requests.post(
            f"{base_url}/answer",
            data={"level": str(task_number), "answer": str(self.result)},
            cookies={"session": cookie},
        )

        text = r.content.decode().split("article")[1]
        if "gold star" in text:
            print(Colors.okgreen(f"Correct solution! I'm one GOLD STAR {'🌟' * task_number} closer to Christmas!"))
            if "Continue to Part Two" in text:
                url_part2 = f"{base_url}#part2"
                print(f"Go to {Colors.bold(url_part2)}")
        if "not the right answer" in text:
            print(text)
            print(Colors.fail("Not the right answer!"))

    def solve_examples(
        self, task_number: int, solution: Optional[int | str | Sequence[int | str]], verbose: bool = True
    ):
        """
        Solve for example inputs and compares to expected results.
        Allows multiple input files named like `<N>_input_example.txt, <N>_input_example_1.txt,...`

        Parameters
        ----------
        task_number :
            number of currently running Part, either 1 or 2
        example_solutions :
            - correct solution for example input of a single task
            - if there are multiple example inputs, it might be a list or tuple
        verbose :
            if True (default), allow all prints
            if False, remove all printing from the output
        """
        print("=" * 15)
        print(f"Task {task_number} - Example")

        if solution is None:
            raise ValueError("You did not provide any solution!")
        elif isinstance(solution, (int, str)):
            solution_list = [solution]
        else:
            solution_list = solution

        path_extensions = [""] + [f"_{i}" for i in range(1, len(solution_list))]
        example_input_paths = [self.example_path_template.format(ext) for ext in path_extensions]

        for sol, path in zip(solution_list, example_input_paths):
            self.load_input(path)
            self.print_input()
            result, run_time = self.run_task(task_number, verbose)
            print(f"Elapsed time: {run_time * 1000:,.1f} ms")
            if result != sol:
                print(Colors.fail("Incorrect solution!"))
                print(f"Should get:  {Colors.okblue(sol)}")
                print(f"Got instead: {Colors.warning(result)}")
            else:
                print(Colors.okgreen("Correct solution!"))
                print(f"Result: {Colors.okblue(result)}")
            print("=" * 15)

    @abstractmethod
    def task_1(self) -> int | str:
        pass

    @abstractmethod
    def task_2(self) -> int | str:
        pass
