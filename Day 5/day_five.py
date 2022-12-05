"""Advent of Code 2022 Day 5"""
from string import ascii_uppercase

from day_five_input import CRATES, INSTRUCTIONS


class CraneMover9000:
    """Representation of Crane used in Part 1"""

    def __init__(self, stacks: list):
        self.stacks = stacks
        self.stacks.insert(0, [])

    def move_crates(self, instruction: str):
        self.__execute_move(*self._parse_instruction(instruction))

    @staticmethod
    def _parse_instruction(instruction: str) -> tuple:
        _, number_of_crates, _, from_stack, _, to_stack = instruction.split()
        return int(number_of_crates), int(from_stack), int(to_stack)

    def __execute_move(self, number_of_crates: int, from_stack: int, to_stack: int):
        for _ in range(number_of_crates):
            self.stacks[to_stack].append(self.stacks[from_stack].pop())

    def get_accesible_crates(self):
        return "".join(stack[-1] for stack in self.stacks[1:])


class CraneMover9001(CraneMover9000):
    """Representation of Crane used in Part 2"""

    def move_crates(self, instruction: str):
        self.__execute_move(*super()._parse_instruction(instruction))

    def __execute_move(self, number_of_crates: int, from_stack: int, to_stack: int):
        self.stacks[to_stack].extend(self.stacks[from_stack][-number_of_crates:])
        self.stacks[from_stack] = self.stacks[from_stack][:-number_of_crates]


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
