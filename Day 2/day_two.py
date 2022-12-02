"""Advent of Code 2022 Day 2 Solution"""
from day_two_input import PUZZLE_INPUT
from rock_paper_scissors import InputProcessor, RockPaperScissors


def main():  # pylint:disable=missing-function-docstring

    game_one = RockPaperScissors()
    for game_round in PUZZLE_INPUT.splitlines():
        player_one, player_two = game_round.split(" ")
        game_one.play_round(
            InputProcessor.decode_item(player_one),
            InputProcessor.decode_item(player_two),
        )

    # ANSWER TO PART 1
    print(game_one.score)

    game_two = RockPaperScissors()
    game_entries = [line.split(" ") for line in PUZZLE_INPUT.splitlines()]
    for player_one, outcome in game_entries:
        player_one = InputProcessor.decode_item(player_one)
        outcome = InputProcessor.decode_outcome(outcome)
        game_two.play_round(player_one, outcome)

    # ANSWER TO PART 2
    print(game_two.score)


if __name__ == "__main__":
    main()
