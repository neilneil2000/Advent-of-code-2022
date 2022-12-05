"""Advent of Code 2022 Day 5"""
from string import ascii_uppercase

from crane_mover import CraneMover9000, CraneMover9001
from day_five_input import CRATES, INSTRUCTIONS


class InputProcessor:
    """Class to Process input from file"""

    @classmethod
    def get_crates(cls, raw_input: str):
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


def main():  # pylint:disable=missing-function-docstring
    instructions = INSTRUCTIONS.splitlines()
    elf_crane = CraneMover9000(InputProcessor.get_crates(CRATES))
    for instruction in instructions:
        elf_crane.move_crates(instruction)
    print(elf_crane.get_accesible_crates())

    elf_crane = CraneMover9001(InputProcessor.get_crates(CRATES))
    for instruction in instructions:
        elf_crane.move_crates(instruction)
    print(elf_crane.get_accesible_crates())


if __name__ == "__main__":
    main()
