"""Solution to Day 4 of Advent of Code 2022"""

from typing import List

from day_four_input import PUZZLE_INPUT
from elf_cleaning_assignment import ElfCleaningAssignment


def process_input() -> List[List[str]]:
    """Process Formatted input into iterable string format"""
    return [pair.split(",") for pair in PUZZLE_INPUT.splitlines()]


def build_elf_list() -> List[List[ElfCleaningAssignment]]:
    """Create list of elf objects"""
    return [
        [ElfCleaningAssignment(elf_one), ElfCleaningAssignment(elf_two)]
        for elf_one, elf_two in process_input()
    ]


def number_of_subsets(elf_pairs: List[ElfCleaningAssignment]):
    """Return number of pairs with a complete overlap (i.e. one is a subset of the other)"""
    return sum(elf_one.is_superset_or_subset(elf_two) for elf_one, elf_two in elf_pairs)


def number_of_overlaps(elf_pairs: List[ElfCleaningAssignment]):
    """Return number of pairs with any overlap"""
    return sum(elf_one.is_overlap(elf_two) for elf_one, elf_two in elf_pairs)


def main():  # pylint:disable=missing-function-docstring
    elf_pairs = build_elf_list()
    print(
        f"{number_of_subsets(elf_pairs)} pairs of elves have a complete overlap"
    )  # PART 1
    print(
        f"{number_of_overlaps(elf_pairs)} pairs of elves have some kind of overlap"
    )  # PART 2


if __name__ == "__main__":
    main()
