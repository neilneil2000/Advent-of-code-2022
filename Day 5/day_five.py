"""Advent of Code 2022 Day 5"""

from crane_mover import CraneMover9000, CraneMover9001
from day_five_input import CRATES, INSTRUCTIONS
from input_processor import InputProcessor


def main():  # pylint:disable=missing-function-docstring
    instructions = INSTRUCTIONS.splitlines()
    elf_crane = CraneMover9000(InputProcessor.process_crate_input(CRATES))
    for instruction in instructions:
        elf_crane.move_crates(instruction)
    print(elf_crane.get_accesible_crates())

    elf_crane = CraneMover9001(InputProcessor.process_crate_input(CRATES))
    for instruction in instructions:
        elf_crane.move_crates(instruction)
    print(elf_crane.get_accesible_crates())


if __name__ == "__main__":
    main()
