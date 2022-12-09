"""Advent of Code 2022 Day 9 Solution"""
from day_nine_input import PUZZLE_INPUT


class Rope:
    """Model of a rope with n segments"""

    def __init__(self, length):
        self.segments = [(0, 0) for _ in range(length)]
        self.tail_visited_locations = {(0, 0)}

    @property
    def head(self):
        """Position of head of rope"""
        return self.segments[0]

    @property
    def body(self):
        """Positions of body of rope (except head)"""
        return self.segments[1:]

    @property
    def tail(self):
        """Position of tail of rope"""
        return self.segments[-1]

    def is_segment_tail(self, segment_number: int):
        """Return True if segment is final segment on rope"""
        return segment_number == len(self.segments) - 1

    def unique_tail_locations(self):
        """Return number of unique locations visited by"""
        return len(self.tail_visited_locations)

    def move_head(self, direction: str):
        """Move Head of rope 1 unit in given direction"""
        x, y = self.segments[0]
        match direction:
            case "U":  # up
                new_position = (x, y + 1)
            case "D":  # down
                new_position = (x, y - 1)
            case "R":  # right
                new_position = (x + 1, y)
            case "L":  # left
                new_position = (x - 1, y)
        self.segments[0] = new_position

    def move_segment(self, segment_number: int):
        """Update position of specific segment"""
        head_x, head_y = self.segments[segment_number - 1]
        tail_x, tail_y = self.segments[segment_number]

        x_displacement = abs(head_x - tail_x)
        y_displacement = abs(head_y - tail_y)

        if x_displacement <= 1 and y_displacement <= 1:
            return

        match x_displacement:
            case 0:
                new_x = tail_x
            case 1:
                new_x = head_x
            case 2:
                new_x = (head_x + tail_x) // 2

        match y_displacement:
            case 0:
                new_y = tail_y
            case 1:
                new_y = head_y
            case 2:
                new_y = (head_y + tail_y) // 2

        self.segments[segment_number] = (new_x, new_y)
        if self.is_segment_tail(segment_number):
            self.tail_visited_locations.add((new_x, new_y))

    def command(self, direction: str, steps: int):
        """Execute a command 'steps' number of times in direction"""
        for _ in range(steps):
            self.move_head(direction)
            for index, _ in enumerate(self.body):
                self.move_segment(index + 1)


def main():  # pylint:disable=missing-function-docstring
    rows = PUZZLE_INPUT.splitlines()
    rope = Rope(10)
    for row in rows:
        direction, steps = row.split()
        rope.command(direction, int(steps))
    print(rope.unique_tail_locations())


if __name__ == "__main__":
    main()
