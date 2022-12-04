"""Solution to Day 4 of Advent of Code 2022"""
from __future__ import annotations

from typing import List

from day_four_input import PUZZLE_INPUT


class ElfCleaningAssignment:
    """Representation of Cleaning Assignment given to an elf"""

    def __init__(self, sectors: str):
        self.start = 0
        self.end = 0
        self.__process_definition(sectors)

    def __process_definition(self, sectors: str):
        """Process 'X-Y' cleaning definition into sectors"""
        self.start, self.end = map(int, sectors.split("-"))

    def is_superset(self, other: ElfCleaningAssignment):
        """Returns True if self is superset of other"""
        return self.start <= other.start and self.end >= other.end

    def is_superset_or_subset(self, other: ElfCleaningAssignment):
        """Returns True if either class is superset of the other"""
        return self.is_superset(other) or other.is_superset(self)

    def is_overlap(self, other: ElfCleaningAssignment):
        """Returns True if there is any overlap between objects"""
        return not (self.start > other.end or self.end < other.start)


def process_input() -> List[List[str]]:
    """Process Formatted input into iterable string format"""
    return [pair.split(",") for pair in PUZZLE_INPUT.splitlines()]


def build_elf_list() -> List[List[ElfCleaningAssignment]]:
    """Create list of elf objects"""
    return [
        [ElfCleaningAssignment(elf_one), ElfCleaningAssignment(elf_two)]
        for elf_one, elf_two in process_input()
    ]


def number_of_subsets(elf_pairs):
    """Return number of pairs with a complete overlap (i.e. one is a subset of the other)"""
    return sum(elf_one.is_superset_or_subset(elf_two) for elf_one, elf_two in elf_pairs)


def number_of_overlaps(elf_pairs):
    """Return number of pairs with any overlap"""
    return sum(elf_one.is_overlap(elf_two) for elf_one, elf_two in elf_pairs)


def main():  # pylint:disable=missing-function-docstring
    elf_pairs = build_elf_list()
    print(number_of_subsets(elf_pairs))  # PART 1
    print(number_of_overlaps(elf_pairs))  # PART 2


if __name__ == "__main__":
    main()
