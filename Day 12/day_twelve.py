"""Advent of Code 2022 Day 12 Solution"""
import sys
from day_twelve_input import EXAMPLE_INPUT, PUZZLE_INPUT


class HeightMap:

    LETTER_TO_HEIGHT = {
        **{chr(ord("a") + n): n + 1 for n in range(26)},
        **{"S": 1, "E": 26},
    }

    def __init__(self, text_map: str):
        self.map = []
        self.distance_map = []
        self.start = ()
        self.end = ()

        text_map = text_map.splitlines()
        for column_id, column in enumerate(text_map):
            temp_row = []
            for row_id, letter in enumerate(column):
                temp_row.append(self.LETTER_TO_HEIGHT[letter])
                if letter == "S":
                    self.start = (row_id, column_id)
                elif letter == "E":
                    self.end = (row_id, column_id)
            self.map.append(temp_row)

        for _ in range(self.map_height):
            temp_row = []
            for _ in range(self.map_width):
                temp_row.append(None)
            self.distance_map.append(temp_row)

    @property
    def map_width(self):
        return len(self.map[0])

    @property
    def map_height(self):
        return len(self.map)

    def __get_neighbours(self, location: tuple):
        """Return co-ordinates of all neightbours of a given location"""
        row, column = location
        neighbours = []
        if row > 0:
            neighbours.append((row - 1, column))
        if row < self.map_width - 1:
            neighbours.append((row + 1, column))
        if column > 0:
            neighbours.append((row, column - 1))
        if column < self.map_height - 1:
            neighbours.append((row, column + 1))
        return neighbours

    def __get_height_at_location(self, location: tuple) -> int:
        row, column = location
        return self.map[column][row]

    def __filter_invalid_steps(self, location: tuple, neighbours: list) -> list:
        valid_next_steps = []
        current_height = self.__get_height_at_location(location)
        for neighbour in neighbours:
            if self.__get_height_at_location(neighbour) >= current_height - 1:
                valid_next_steps.append(neighbour)
        return valid_next_steps

    def solve(self):
        self.flood_fill(self.end, 0)
        column, row = self.start
        return self.distance_map[row][column]

    def flood_fill(self, starting_point: tuple, value: int):
        column, row = starting_point
        if (
            self.distance_map[row][column] is not None
            and self.distance_map[row][column] <= value
        ):
            return
        self.distance_map[row][column] = value
        for next_move in self.get_next_moves(starting_point):
            self.flood_fill(next_move, value + 1)
        return

    def get_next_moves(self, location):
        next_moves = self.__get_neighbours(location)
        next_moves = self.__filter_invalid_steps(location, next_moves)
        return next_moves

    def get_fewest_a_to_z(self):
        """Return fewest number of steps starting at any a level position"""
        column, row = self.start
        fastest_route = self.distance_map[row][column]
        for row_id, row in enumerate(self.map):
            for column_id, height in enumerate(row):
                if height == 1:
                    distance = self.distance_map[row_id][column_id]
                    if distance is not None:
                        fastest_route = min(fastest_route, distance)
        return fastest_route


def main():
    sys.setrecursionlimit(1_000_000)
    landscape = HeightMap(PUZZLE_INPUT)
    print(landscape.solve())
    print(landscape.get_fewest_a_to_z())
    pass


if __name__ == "__main__":
    main()
