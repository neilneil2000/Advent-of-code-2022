"""Input Processor for Advent of Code 2022 Day 5"""
from string import ascii_uppercase


class InputProcessor:
    """Class to Process input from file"""

    @classmethod
    def process_crate_input(cls, raw_input: str):
        """Return formatted list of crates from input format"""
        crates = cls.__initialise_crate_stack(cls.__number_of_crate_stacks(raw_input))
        crate_stack = raw_input.splitlines()[:-1]
        for line in crate_stack:
            for index, character in enumerate(line):
                if character in ascii_uppercase:
                    crates[(index - 1) // 4].append(character)

        return [stack[::-1] for stack in crates]

    @staticmethod
    def __initialise_crate_stack(number_of_stacks: int) -> list:
        return [[] for _ in range(number_of_stacks)]

    @staticmethod
    def __number_of_crate_stacks(raw_input: str) -> int:
        return int(raw_input.splitlines()[-1].split()[-1])
