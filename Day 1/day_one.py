""" Solution to Day 1 Advent of Code 2022"""
from day_one_input import puzzle_input


def process_input(puzzle_input: str) -> list:
    """Process Multi-line input string to list of lists"""
    return [elf.splitlines() for elf in puzzle_input.split("\n\n")]


def summarise_entries(lists: list) -> list:
    """Takes a 2D array and computes the sum on each sublist"""
    return [sum_list(entry) for entry in lists]


def sum_list(my_list: list) -> int:
    """Returns integer sum of values in list"""
    return sum(int(entry) for entry in my_list)


def main():  # pylint:disable=missing-function-docstring
    food_items_by_elf = process_input(puzzle_input)
    calories_by_elf = summarise_entries(food_items_by_elf)
    calories_by_elf.sort()

    # ANSWER TO PART 1
    print(calories_by_elf[-1])

    # ANSWER TO PART 2
    print(sum(calories_by_elf[-3:]))


if __name__ == "__main__":
    main()
