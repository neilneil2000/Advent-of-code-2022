"""File System Model for Advent of Code 2022 Day 7"""
from dataclasses import dataclass, field
from typing import Protocol


class FileSystemObject(Protocol):
    """Protocol defining a file system object"""

    name: str
    size: int


@dataclass
class File:
    """Representation of  File"""

    name: str
    size: int

    def display(self, indent_level: int):
        print(" " * indent_level, end="")
        print(f"- {self.name} {self.size}")


@dataclass
class Directory:
    """Representation of a Directory"""

    name: str
    contents: dict = field(default_factory=dict)

    @property
    def size(self) -> int:
        """Return size contained within directory"""
        return sum(item.size for item in self.contents.values())

    def add_item(self, item: FileSystemObject):
        """Add an item into the directory"""
        if self.contents.get(item.name) is not None:
            raise ValueError("Item with that name already exists")
        self.contents[item.name] = item

    def get_directory_sizes(self, sizes: list):
        for item in self.contents.values():
            if isinstance(item, Directory):
                item.get_directory_sizes(sizes)
        sizes.append(self.size)
        return sizes

    def display(self, indent_level: int):
        """Display Directory recursively"""
        print(" " * indent_level, end="")
        print(f"- {self.name} (dir) {self.size}")
        for item in self.contents.values():
            item.display(indent_level + 1)

    def sum_directories(self, exclude_over: int):
        """Return sum of directory sizes that are not of greater size than 'exclude_over'"""
        total = 0
        for item in self.contents.values():
            if isinstance(item, Directory):
                total += item.sum_directories(exclude_over)
                if item.size <= exclude_over:
                    total += item.size
        return total


class FileSystem:
    """Representation of a file system"""

    def __init__(self, total_disk_space=None):
        self.root = Directory("/")
        self.position_pointer = [self.root]
        self.total_disk_space = total_disk_space

    @property
    def cwd(self):
        """Return Current Working Directory"""
        return self.position_pointer[-1]

    def add_item(self, add_item_command: str):
        """Add item at current level in hierarchy"""
        add_item_command = add_item_command.split()
        if add_item_command[0] == "dir":
            self.cwd.add_item(Directory(add_item_command[1]))
        else:
            self.cwd.add_item(File(add_item_command[1], int(add_item_command[0])))

    def change_directory(self, new_directory: str):
        """Change directory level"""
        if new_directory == "..":
            self.position_pointer.pop()
            return
        if new_directory == "/":
            self.position_pointer = [self.root]
            return
        if self.cwd.contents.get(new_directory) is None:
            raise LookupError("Directory not found")
        self.position_pointer.append(self.cwd.contents[new_directory])

    def display(self):
        """Prints file structure to screen"""
        self.root.display(indent_level=0)

    def get_directory_sizes(self):
        """Return list of all directory sizes"""
        return self.root.get_directory_sizes([])

    def smallest_directory_to_delete(self, target_space: int) -> int:
        """Returns size of smallest_directory that can be deleted to generate target_space"""
        space_needed = target_space + self.root.size - self.total_disk_space
        directory_sizes = sorted(self.get_directory_sizes())
        for size in directory_sizes:
            if size > space_needed:
                return size
        return 0

    def sum_directories(self, exclude_over: int):
        return self.root.sum_directories(exclude_over)
