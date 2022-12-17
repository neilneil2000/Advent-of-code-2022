from day_seventeen_input import EXAMPLE_INPUT, PUZZLE_INPUT
from rocks import RockFactory
from chamber import Chamber
from pattern_finder import find_pattern


def main():  # pylint:disable=missing-function-docstring
    chamber_width = 7
    blocks_to_drop = 10_000
    chamber_of_doom = Chamber(RockFactory(), chamber_width, PUZZLE_INPUT)
    for block_index in range(blocks_to_drop):
        chamber_of_doom.do_block_cycle()
        if (block_index + 1) % 100_000 == 0:
            print(f"{block_index+1} blocks simulated", end="\r")
    print(f"Tower Height: {max(chamber_of_doom.floor)-1} after {blocks_to_drop} blocks")
    heights = list(reversed(chamber_of_doom.heights))
    find_pattern(heights)
    incs = []
    for index in range(784, 10_000, 860):
        incs.append(heights[index])
    print(incs)
    incs = []
    for index in range(75, 10_000, 2345):
        incs.append(heights[index])
    print(incs)
    print(chamber_of_doom.heights[8320])


if __name__ == "__main__":
    main()
