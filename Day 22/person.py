from grove import Grove
from cube_grove import CubeGrove


class Walker:
    """Representation of a Person"""

    TURNS = {
        "L": {"R": "U", "D": "R", "L": "D", "U": "L"},
        "R": {"R": "D", "D": "L", "L": "U", "U": "R"},
    }

    def __init__(self, grove: CubeGrove, directions: list) -> None:
        self.grove = grove
        self.directions = directions
        self.location = self.get_starting_point()
        self.orientation = "R"

    def orientation_value(self):
        match self.orientation:
            case "R":
                return 0
            case "D":
                return 1
            case "L":
                return 2
            case "U":
                return 3

    def password(self):
        column, row = self.location
        column += 1
        row += 1
        return 1000 * row + 4 * column + self.orientation_value()

    def get_starting_point(self) -> tuple:
        """Return starting co-ordinates"""
        return self.grove.get_top_left_most_location()

    def turn(self, turn_instruction: str) -> None:
        """"""
        self.orientation = self.TURNS[turn_instruction][self.orientation]

    def try_next_forward_step(self) -> tuple:
        """
        Move forward one space and update location
        Returns location after doing step
        If cannot move then location returned will be current location
        """
        next_location, new_orientation = self.grove.get_location_and_orientation(
            self.location, self.orientation
        )
        if self.grove.get_square_content(next_location) == "#":
            return self.location
        self.orientation = new_orientation
        return next_location

    def get_next_location(self) -> tuple:
        x, y = self.location
        match self.orientation:
            case "L":
                x -= 1
            case "R":
                x += 1
            case "U":
                y -= 1
            case "D":
                y += 1
        return (x, y)

    def move(self, move_instruction: int) -> None:
        x, y = self.location
        for _ in range(move_instruction):
            x, y = self.try_next_forward_step()
            if self.location == (x, y):
                break
            self.location = (x, y)

    def follow_directions(self) -> None:
        for instruction in self.directions:
            if instruction in ["L", "R"]:
                self.turn(instruction)
            else:
                self.move(instruction)
