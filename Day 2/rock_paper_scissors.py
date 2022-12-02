"""Supporting Classes for Rock, Paper, Scissors Game"""
from enum import Enum


class Item(Enum):
    """Player Items used in Rock, Paper, Scissors and their respective scores"""

    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Outcome(Enum):
    """Game Outcomes in Rock, Paper, Scissors and their respective scores"""

    WIN = 6
    DRAW = 3
    LOSE = 0


class RockPaperScissors:
    """Rock, Paper, Scissors Game Emulator"""

    def __init__(self):
        self.score = 0

    def __update_score(self, outcome: Outcome, player_choice: Item):
        """Update the cumulative score based on game outcome and item"""
        self.score += outcome.value + player_choice.value

    def play_round(self, input_a: Enum, input_b: Enum):
        if isinstance(input_b, Item):
            self.__play_round_part_1(input_a, input_b)
            return
        self.__play_round_part_2(input_a, input_b)

    def __play_round_part_1(self, player_one: Item, player_two: Item):
        """Play a Round of Rock, Paper, Scissors"""
        if player_one == player_two:
            return self.__update_score(Outcome.DRAW, player_two)
        if (
            (player_one == Item.ROCK and player_two == Item.PAPER)
            or (player_one == Item.PAPER and player_two == Item.SCISSORS)
            or (player_one == Item.SCISSORS and player_two == Item.ROCK)
        ):
            return self.__update_score(Outcome.WIN, player_two)
        return self.__update_score(Outcome.LOSE, player_two)

    def __play_round_part_2(self, player_one: Item, round_outcome: Outcome):
        """Play a Round of Rock, Paper, Scissors as defined in part 2 of the problem"""
        if round_outcome == Outcome.DRAW:
            return self.__update_score(round_outcome, player_one)
        if round_outcome == Outcome.WIN:
            return self.__update_score(
                round_outcome, self.__item_that_beats(player_one)
            )
        return self.__update_score(round_outcome, self.__item_that_loses(player_one))

    @staticmethod
    def __item_that_beats(item: Item) -> Item:
        """Return the item that beats the one provided"""
        if item == Item.ROCK:
            return Item.PAPER
        if item == Item.PAPER:
            return Item.SCISSORS
        return Item.ROCK

    @staticmethod
    def __item_that_loses(item: Item) -> Item:
        """Return the item that loses to the one provided"""
        if item == Item.ROCK:
            return Item.SCISSORS
        if item == Item.PAPER:
            return Item.ROCK
        return Item.PAPER


class InputProcessor:
    """Processes Puzzle inputs from ASCII to defined Enumerations"""

    ROCKS = ("A", "X")
    PAPER = ("B", "Y")
    SCISSORS = ("C", "Z")

    LOSE = "X"
    DRAW = "Y"
    WIN = "Z"

    @classmethod
    def decode_item(cls, encoded_item: str) -> Item:
        """Return Item Enumeration for ASCII encoded outcome"""
        if encoded_item in cls.ROCKS:
            return Item.ROCK
        if encoded_item in cls.PAPER:
            return Item.PAPER
        return Item.SCISSORS

    @classmethod
    def decode_outcome(cls, encoded_item: str) -> Outcome:
        """Return Outcome Enumeration for ASCII encoded outcome"""
        if encoded_item in cls.LOSE:
            return Outcome.LOSE
        if encoded_item in cls.DRAW:
            return Outcome.DRAW
        return Outcome.WIN
