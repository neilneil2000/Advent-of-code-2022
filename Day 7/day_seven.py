"Advent of Code 2022 Day 7 Solution"
from day_seven_input import PUZZLE_INPUT
from file_system import FileSystem


class CommandExecutor:
    """Module to Execute File System Commands"""

    CHANGE_DIRECTORY = "cd"
    LIST_CONTENTS = "ls"

    @classmethod
    def run_command(cls, command: str, file_system: FileSystem):
        """Execute the command to build File Structure"""
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

    # PART 1
    print(elf_device.sum_directories(exclude_over=100_000))

    # PART 2
    total_disk = 70_000_000
    space_required = 30_000_000

    elf_device.total_disk_space = total_disk
    print(elf_device.smallest_directory_to_delete(space_required))


if __name__ == "__main__":
    main()
