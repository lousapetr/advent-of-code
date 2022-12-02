from wrapper import Wrapper

# https://adventofcode.com/2021/day/2


class Solver(Wrapper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.parser = self.parse_to_list
        self.input = super().load_input()

    @staticmethod
    def remap_hands(orig_hands: list, hands_map: dict):
        output = orig_hands.copy()
        for orig, new in hands_map.items():
            output = [hand.replace(orig, new) for hand in output]
        return output

    @staticmethod
    def get_hand_score(hand: str):
        """
        match = '[ABC] [ABC]'
            - remapped hands
            - first is opponent, second myself

        output = score
            - A=1, B=2, C=3
            - A>C, B>A, C>B
                - 0 for lose, 3 for draw, 6 for win
        """
        hand = hand.replace(" ", "")

        letter_score_map = {"A": 1, "B": 2, "C": 3}
        letter_score = letter_score_map[hand[1]]

        if hand[0] == hand[1]:
            output_score = 3
        elif hand in ("AB", "BC", "CA"):
            output_score = 6
        else:
            output_score = 0

        return letter_score + output_score

    def get_total_score(self, hands: list):
        return sum(self.get_hand_score(h) for h in hands)

    def task_1(self):
        hand_map = {"X": "A", "Y": "B", "Z": "C"}
        mapped_hands = self.remap_hands(self.input, hand_map)
        return self.get_total_score(mapped_hands)

    @staticmethod
    def find_hand(orig_line: str):
        """
        X = lose, Y = draw, Z = win

        return correct hands combination for desired output
        """
        orig_line = orig_line.replace(" ", "")
        opponent = orig_line[0]
        desired = orig_line[1]

        loses = {"A": "C", "B": "A", "C": "B"}  # winner: loser
        wins = {loser: winner for winner, loser in loses.items()}

        if desired == "Y":
            return f"{opponent} {opponent}"
        elif desired == "X":
            return f"{opponent} {loses[opponent]}"
        elif desired == "Z":
            return f"{opponent} {wins[opponent]}"
        else:
            raise ValueError("invalid desired output")

    def task_2(self):
        played_hands = [self.find_hand(hand) for hand in self.input]
        return self.get_total_score(played_hands)


part = 2
solve_example = False
example_solutions = [15, 12]

solver = Solver(day=2, example=solve_example, example_solutions=example_solutions)
if solve_example:
    solver.print_input()
solver.solve_task(1)
if part > 1:
    solver.solve_task(2)