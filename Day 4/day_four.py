"""Solution to Day 4 of Advent of Code 2022"""
from typing import List
from day_four_input import PUZZLE_INPUT


class ElfCleaningAssignment:
    """Representation of Cleaning Assignment given to an elf"""

    def __init__(self, definition: str):
        self.start = 0
        self.end = 0
        self.__process_definition(definition)

    def __process_definition(self, definition: str):
        """Process X-Y cleaning definition into areas"""
        start, end = definition.split("-")
        self.start = int(start)
        self.end = int(end)

    def is_superset(self, other):
        """Returns True if self is superset of other"""
        return self.start <= other.start and self.end >= other.end

    def is_superset_or_subset(self, other):
        """Returns True if either class is superset of the other"""
        return self.is_superset(other) or other.is_superset(self)

    def is_overlap(self, other):
        """Returns True if there is any overlap between objects"""
        return not (self.start > other.end or self.end < other.start)


def process_input() -> List[List[str]]:
    """Process Formatted input into iterable string format"""
    return [pair.split(",") for pair in PUZZLE_INPUT.splitlines()]


def main():  # pylint:disable=missing-function-docstring
    elf_pairs = []
    for elf_one, elf_two in process_input():
        elf_pairs.append(
            [ElfCleaningAssignment(elf_one), ElfCleaningAssignment(elf_two)]
        )
    print(sum(elf_one.is_superset_or_subset(elf_two) for elf_one, elf_two in elf_pairs))
    print(sum(elf_one.is_overlap(elf_two) for elf_one, elf_two in elf_pairs))


if __name__ == "__main__":
    main()
