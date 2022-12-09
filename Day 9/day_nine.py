"""Advent of Code 2022 Day 9 Solution"""
from day_nine_input import PUZZLE_INPUT


class Rope:
    """Model of a rope of length 'length'"""

    def __init__(self, length):
        self.segments = [(0, 0) for _ in range(length)]
        self.tail_visited_locations = {(0, 0)}

    @property
    def __body(self):
        """Positions of body of rope (except head)"""
        return self.segments[1:]

    def __is_segment_tail(self, segment_number: int):
        """Return True if segment is final segment on rope"""
        return segment_number == len(self.segments) - 1

    def unique_tail_locations(self):
        """Return number of unique locations visited by"""
        return len(self.tail_visited_locations)

    def __move_head(self, direction: str):
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

    def __needs_to_move(self, segment_number: int):
        """Returns True if segment needs to move"""
        head_x, head_y = self.segments[segment_number - 1]
        tail_x, tail_y = self.segments[segment_number]

        x_displacement = abs(head_x - tail_x)
        y_displacement = abs(head_y - tail_y)

        return x_displacement > 1 or y_displacement > 1

    def __move_segment(self, segment_number: int):
        """Update position of specific segment"""
        head_x, head_y = self.segments[segment_number - 1]
        tail_x, tail_y = self.segments[segment_number]

        if not self.__needs_to_move(segment_number):
            return

        new_x = self.__get_new_position(head_x, tail_x)
        new_y = self.__get_new_position(head_y, tail_y)

        self.__update_segment_position(segment_number, (new_x, new_y))

    def __update_segment_position(self, segment_number, segment_position):
        """Store new position for segment"""
        self.segments[segment_number] = segment_position
        if self.__is_segment_tail(segment_number):
            self.tail_visited_locations.add(segment_position)

    def __get_new_position(self, head, tail):
        """Return new position of tail on one-dimensional axis given position of head"""
        match abs(head - tail):
            case 0:
                return tail
            case 1:
                return head
        return (head + tail) // 2

    def run_command(self, direction: str, steps: int):
        """Execute a command 'steps' number of times in direction"""
        for _ in range(steps):
            self.__move_head(direction)
            for index, _ in enumerate(self.__body):
                self.__move_segment(index + 1)


def main():  # pylint:disable=missing-function-docstring
    rows = PUZZLE_INPUT.splitlines()
    ROPE_SEGMENTS = 10
    rope = Rope(ROPE_SEGMENTS)
    for row in rows:
        direction, steps = row.split()
        rope.run_command(direction, int(steps))
    print(rope.unique_tail_locations())


if __name__ == "__main__":
    main()
