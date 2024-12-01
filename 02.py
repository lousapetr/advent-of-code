from collections import Counter

from wrapper import Wrapper

# --- Day 2: Cube Conundrum ---
# https://adventofcode.com/2023/day/2

DAY_NUMBER = 2


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_to_list

    @staticmethod
    def parse_line(line: str):
        game_id, draws_raw = line.split(":")
        game_id = int(game_id.split()[-1])

        draws_list = draws_raw.split(";")
        draws = []
        for d in draws_list:
            draw = {}
            for c in d.split(","):
                n, cube = c.split()
                draw[cube.strip()] = int(n)
            draws.append(Counter(draw))
        return game_id, draws

    def parse_input_lines(self):
        return [self.parse_line(line) for line in self.input]

    def task_1(self):
        parsed_input = self.parse_input_lines()
        bag = Counter({"red": 12, "green": 13, "blue": 14})
        possible_games = []
        for game_id, draws in parsed_input:
            # if draw is larger than the bag, it's invalid
            if not any(d - bag for d in draws):
                possible_games.append(game_id)
                print(game_id)
                print(draws)
        print(possible_games)
        return sum(possible_games)

    def task_2(self):
        powers = []
        for game_id, draws in self.parse_input_lines():
            minimum_set = Counter()
            for d in draws:
                minimum_set |= d
            print(game_id)
            print(minimum_set)
            power = 1
            for n in minimum_set.values():
                power *= n
            print(power)
            powers.append(power)
        return sum(powers)


part = 2
solve_example = True
solve_example = False
example_solutions = [8, 2286]

solver = Solver(day=DAY_NUMBER, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1, verbose=False)
if part > 1:
    solver.solve_task(2)
