"""Advent of Code 2022 Day 5"""
from day_five_input import INSTRUCTIONS


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


#        [H]     [W] [B]
#    [D] [B]     [L] [G] [N]
# [P] [J] [T]     [M] [R] [D]
# [V] [F] [V]     [F] [Z] [B]     [C]
# [Z] [V] [S]     [G] [H] [C] [Q] [R]
# [W] [W] [L] [J] [B] [V] [P] [B] [Z]
# [D] [S] [M] [S] [Z] [W] [J] [T] [G]
# [T] [L] [Z] [R] [C] [Q] [V] [P] [H]
# 1   2   3   4   5   6   7   8   9


def get_crates():
    crates = []
    crates.append(["T", "D", "W", "Z", "V", "P"])
    crates.append(["L", "S", "W", "V", "F", "J", "D"])
    crates.append(["Z", "M", "L", "S", "V", "T", "B", "H"])
    crates.append(["R", "S", "J"])
    crates.append(["C", "Z", "B", "G", "F", "M", "L", "W"])
    crates.append(["Q", "W", "V", "H", "Z", "R", "G", "B"])
    crates.append(["V", "J", "P", "C", "B", "D", "N"])
    crates.append(["P", "T", "B", "Q"])
    crates.append(["H", "G", "Z", "R", "C"])
    return crates


def main():
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
