"Advent of Code 2022 Day 7 Solution"
from day_seven_input import PUZZLE_INPUT, EXAMPLE_PUZZLE_INPUT
from file_system import FileSystem


class CommandExecutor:

    CHANGE_DIRECTORY = "cd"
    LIST_CONTENTS = "ls"

    @classmethod
    def run_command(cls, command: str, file_system: FileSystem):
        if command == "":
            return
        command, *output = command.splitlines()
        command = command.split()
        if command[0] == cls.CHANGE_DIRECTORY:
            file_system.change_directory(command[1])
        elif command[0] == cls.LIST_CONTENTS:
            for item in output:
                file_system.add_item(item)


def main():  # pylint:disable=missing-function-docstring
    commands = PUZZLE_INPUT.split("$")
    elf_device = FileSystem()
    for command in commands:
        CommandExecutor.run_command(command, elf_device)
    # print(elf_device.sum_items(100_000))
    total = 0
    for dir_size in elf_device.get_directory_sizes():
        if dir_size <= 100_000:
            total += dir_size
    print(total)
    # elf_device.display()


if __name__ == "__main__":
    main()
