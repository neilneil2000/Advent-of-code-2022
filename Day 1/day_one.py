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


def sum_sub_lists(lists: list) -> list:
    """Takes a 2D array and computes the sum on each sublist"""
    totals = []
    temp_sum = 0
    for entry in lists:
        for number in entry:
            temp_sum += int(number)
        totals.append(temp_sum)
        temp_sum = 0
    return totals


def main():  # pylint:disable=missing-function-docstring
    input_list = puzzle_input.splitlines()
    split_list = split_list_by_blank_strings(input_list)
    summary_list = sum_sub_lists(split_list)
    summary_list.sort()

    # ANSWER TO PART 1
    print(summary_list[-1])

    # ANSWER TO PART 2
    print(sum(summary_list[-3:]))


if __name__ == "__main__":
    main()
