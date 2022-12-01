""" Solution to Day 1 Advent of Code 2022"""
from typing import List

from day_one_input import puzzle_input


def process_input(multiline_input: str) -> List[List[str]]:
    """Process Multi-line input string to list of lists"""
    return [sub_list.splitlines() for sub_list in multiline_input.split("\n\n")]


def summarise_entries(lists: List[List[str]]) -> List[int]:
    """Takes a 2D array and computes the sum on each sublist"""
    return [sum_list(entry) for entry in lists]


def sum_list(my_list: List[str]) -> int:
    """Returns integer sum of values in list"""
    return sum(int(entry) for entry in my_list)


def sum_highest_values(my_list: List[int], number_of_values: int = 1) -> int:
    """
    Returns sum of highest values in a list
    number_of_values is number of values to consider
    Default is to return single highest value
    """
    return sum(sorted(my_list)[-number_of_values:])


def main():  # pylint:disable=missing-function-docstring
    food_items_by_elf = process_input(puzzle_input)
    calories_by_elf = summarise_entries(food_items_by_elf)

    # ANSWER TO PART 1
    part_one = sum_highest_values(calories_by_elf, 1)
    print(part_one)

    # ANSWER TO PART 2
    part_two = sum_highest_values(calories_by_elf, 3)
    print(part_two)


if __name__ == "__main__":
    main()
