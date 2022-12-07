"Advent of Code 2022 Day 7 Solution"

from dataclasses import dataclass, field

from day_seven_input import PUZZLE_INPUT
from file_system import FileSystem


class CommandExecutor:
    """Module to Execute File System Commands"""

    CHANGE_DIRECTORY = "cd"
    LIST_CONTENTS = "ls"

    @dataclass
    class Command:
        """Representation of Command"""

        name: str
        arguments: field(default_factory=list) = None
        output: field(default_factory=list) = None

    @classmethod
    def run_command(cls, command_string: str, file_system: FileSystem) -> None:
        """Execute the command to build File Structure"""
        command = cls.parse_command(command_string)
        match command.name:
            case cls.CHANGE_DIRECTORY:
                cls.execute_change_directory(command, file_system)
            case cls.LIST_CONTENTS:
                cls.execute_list_contents(command, file_system)

    @classmethod
    def parse_command(cls, command_string: str) -> Command:
        """Parse command multiline string into Command Object"""
        if command_string == "":
            return cls.Command(name="")
        command_input, *command_output = command_string.splitlines()
        command_input = command_input.split()
        new_command = cls.Command(name=command_input.pop(0))
        if command_input:
            new_command.arguments = command_input
        if command_output:
            new_command.output = command_output
        return new_command

    @staticmethod
    def execute_list_contents(command: Command, file_system: FileSystem) -> None:
        """Execute a List Contents Command"""
        for item in command.output:
            file_system.add_item(item)

    @staticmethod
    def execute_change_directory(command: Command, file_system: FileSystem) -> None:
        """Execute a Change Directory Command"""
        file_system.change_directory(command.arguments[0])


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
