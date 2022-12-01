""" Solution to Day 1 Advent of Code 2022"""
from day_one_input import puzzle_input


def split_list_by_blank_strings(input_list: list) -> list:
    """
    Uses blank string entries in a list as a delimiter
    Returns List of Lists
    """
    output_list = []
    temp_list = []
    for item in input_list:
        if item == "":
            output_list.append(temp_list)
            temp_list = []
        else:
            temp_list.append(item)

    return output_list


def summarise_entries(lists: list) -> list:
    """Takes a 2D array and computes the sum on each sublist"""
    return [sum_list(entry) for entry in lists]


def sum_list(my_list: list) -> int:
    """Returns integer sum of values in list"""
    return sum(int(entry) for entry in my_list)


def main():  # pylint:disable=missing-function-docstring
    food_items_by_elf = split_list_by_blank_strings(puzzle_input.splitlines())
    calories_by_elf = summarise_entries(food_items_by_elf)
    calories_by_elf.sort()

    # ANSWER TO PART 1
    print(calories_by_elf[-1])

    # ANSWER TO PART 2
    print(sum(calories_by_elf[-3:]))


if __name__ == "__main__":
    main()
