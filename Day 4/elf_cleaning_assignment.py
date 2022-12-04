"""Elf Cleaning Assignment Class for Day 4 of Advent of Code 2022"""

from __future__ import annotations


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
