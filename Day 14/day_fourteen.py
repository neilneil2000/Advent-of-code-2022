from functools import lru_cache
from day_fourteen_input import EXAMPLE_INPUT, PUZZLE_INPUT


class Cave:

    ENTRY_POINT = (500, 0)  # Point at which sand enters cave

    def __init__(self, rocks: set):
        self.rocks = rocks
        self.__floor_level = self.__maximum_depth + 2

    @property
    def __maximum_depth(self):
        """Returns the y co-ordinate of the lowest rock"""
        return max(y for _, y in self.rocks)

    def is_on_floor(self, position: tuple):
        """Returns true if location is on floor of cave"""
        _, y = position  # pylint:disable=invalid-name
        return y == self.__floor_level - 1

    @staticmethod
    def get_next_positions(current_position: tuple):
        """Return ordered list of next positions to try"""
        x, y = current_position  # pylint:disable=invalid-name
        return [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]

    def __get_landing_place_with_floor(self, sand_position: tuple, obstacles: set):
        """Returns the landing place of the sand in an environment with a floor"""
        if self.is_on_floor(sand_position):
            return sand_position

        for position in self.get_next_positions(sand_position):
            if position not in obstacles:
                return self.__get_landing_place_with_floor(position, obstacles)

        return sand_position

    def __get_landing_place_with_abyss(self, sand_position: tuple, obstacles: set):
        """Returns the landing place of the sand in an environment with a floor"""
        if self.is_on_floor(sand_position):
            return (-1, -1)

        for position in self.get_next_positions(sand_position):
            if position not in obstacles:
                return self.__get_landing_place_with_abyss(position, obstacles)

        return sand_position

    def get_amount_of_sand_before_abyss(self):
        """Return amount of sand that will collect before it pours into the abyss"""
        landing_position = (0, 0)
        sand = set()
        while landing_position != (-1, -1):
            landing_position = self.__get_landing_place_with_abyss(
                sand_position=self.ENTRY_POINT, obstacles=self.rocks | sand
            )
            sand.add(landing_position)
        return len(sand) - 1

    def get_amount_of_sand_before_blocked(self):
        """Return amount of sand that will collect before the entry point is blocked"""
        landing_position = (0, 0)
        sand = set()
        while landing_position != self.ENTRY_POINT:
            landing_position = self.__get_landing_place_with_floor(
                sand_position=self.ENTRY_POINT, obstacles=self.rocks | sand
            )
            sand.add(landing_position)
        return len(sand)


def get_rocks_in_line(start, end):
    """Returns set of rocks in line"""
    rocks = {start, end}
    x_start, y_start = start
    x_end, y_end = end
    if x_start == x_end:
        for y in range(min(y_start, y_end), max(y_start, y_end) + 1):
            rocks.add((x_start, y))
    else:
        for x in range(min(x_start, x_end), max(x_start, x_end) + 1):
            rocks.add((x, y_start))

    return rocks


def get_rock_positions(rock_lines: list):
    """Returns set of rock positions"""
    rocks = set()
    starting_rock = rock_lines.pop(0)
    for rock_end in rock_lines:
        rocks = rocks.union(get_rocks_in_line(starting_rock, rock_end))
        starting_rock = rock_end
    return rocks


def main():  # pylint:disable=missing-function-docstring
    puzzle = [line.split(" -> ") for line in PUZZLE_INPUT.splitlines()]
    rocks = set()
    for rock_formation in puzzle:
        line = [tuple(map(int, x.split(","))) for x in rock_formation]
        rocks = rocks.union(get_rock_positions(line))

    cave = Cave(rocks)
    part_one = cave.get_amount_of_sand_before_abyss()
    print(part_one)
    part_two = cave.get_amount_of_sand_before_blocked()
    print(part_two)


if __name__ == "__main__":
    main()
