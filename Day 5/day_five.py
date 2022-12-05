"""Advent of Code 2022 Day 5"""
from string import ascii_uppercase

from crane_mover import CraneMover9000, CraneMover9001
from day_five_input import CRATES, INSTRUCTIONS


def get_crates():
    """Return formatted list of crates from input format"""
    crates = [[] for _ in range(9)]
    crate_stack = CRATES.splitlines()
    for line in crate_stack:
        for index, character in enumerate(line):
            if character in ascii_uppercase:
                crates[(index - 1) // 4].append(character)

    return [stack[::-1] for stack in crates]


def main():  # pylint:disable=missing-function-docstring
    instructions = INSTRUCTIONS.splitlines()
    elf_crane = CraneMover9000(get_crates())
    for instruction in instructions:
        elf_crane.move_crates(instruction)
    print(elf_crane.get_accesible_crates())

    elf_crane = CraneMover9001(get_crates())
    for instruction in instructions:
        elf_crane.move_crates(instruction)
    print(elf_crane.get_accesible_crates())


if __name__ == "__main__":
    main()
