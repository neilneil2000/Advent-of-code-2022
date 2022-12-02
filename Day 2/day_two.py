from enum import Enum

from day_two_input import PUZZLE_INPUT


class Item(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Outcome(Enum):
    WIN = 6
    DRAW = 3
    LOSE = 0


class RockPaperScissors:
    def __init__(self):
        self.player_two_score = 0

    def update_score(self, outcome: Outcome, player_choice: Item):
        self.player_two_score += outcome.value + player_choice.value

    def play_round(self, player_one: Item, player_two: Item):
        if player_one == player_two:
            return self.update_score(Outcome.DRAW, player_two)
        if (
            (player_one == Item.ROCK and player_two == Item.PAPER)
            or (player_one == Item.PAPER and player_two == Item.SCISSORS)
            or (player_one == Item.SCISSORS and player_two == Item.ROCK)
        ):
            return self.update_score(Outcome.WIN, player_two)
        self.update_score(Outcome.LOSE, player_two)

    def play_round_part_2(self, player_one: Item, round_outcome: Outcome):
        if round_outcome == Outcome.DRAW:
            return self.update_score(round_outcome, player_one)
        if round_outcome == Outcome.WIN:
            return self.update_score(round_outcome, self.item_that_beats(player_one))
        return self.update_score(round_outcome, self.item_that_loses(player_one))

    @staticmethod
    def item_that_beats(item: Item) -> Item:
        if item == Item.ROCK:
            return Item.PAPER
        if item == Item.PAPER:
            return Item.SCISSORS
        return Item.ROCK

    @staticmethod
    def item_that_loses(item: Item) -> Item:
        if item == Item.ROCK:
            return Item.SCISSORS
        if item == Item.PAPER:
            return Item.ROCK
        return Item.PAPER


class InputProcessor:

    ROCKS = ("A", "X")
    PAPER = ("B", "Y")
    SCISSORS = ("C", "Z")

    LOSE = "X"
    DRAW = "Y"
    WIN = "Z"

    @classmethod
    def decode_item(cls, encoded_item: str) -> Item:
        if encoded_item in cls.ROCKS:
            return Item.ROCK
        if encoded_item in cls.PAPER:
            return Item.PAPER
        if encoded_item in cls.SCISSORS:
            return Item.SCISSORS

    @classmethod
    def decode_outcome(cls, encoded_item: str) -> Item:
        if encoded_item in cls.LOSE:
            return Outcome.LOSE
        if encoded_item in cls.DRAW:
            return Outcome.DRAW
        if encoded_item in cls.WIN:
            return Outcome.WIN


def main():

    game_one = RockPaperScissors()
    for game_round in PUZZLE_INPUT.splitlines():
        player_one, outcome = game_round.split(" ")
        game_one.play_round(
            InputProcessor.decode_item(player_one),
            InputProcessor.decode_item(outcome),
        )

    # ANSWER TO PART 1
    print(game_one.player_two_score)

    game_two = RockPaperScissors()
    for game_round in PUZZLE_INPUT.splitlines():
        player_one, outcome = game_round.split(" ")
        game_two.play_round_part_2(
            InputProcessor.decode_item(player_one),
            InputProcessor.decode_outcome(outcome),
        )

    # ANSWER TO PART 2
    print(game_two.player_two_score)


if __name__ == "__main__":
    main()
