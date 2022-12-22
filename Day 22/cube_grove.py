class CubeGrove:
    """Representation of a grove"""

    def __init__(self, layout: list):
        self.layout = layout

    def get_top_left_most_location(self):
        """Returns first viable location on first row"""
        return (self.layout[0].find("."), 0)

    def is_viable_location(self, location: tuple) -> bool:
        """Returns True if location exists in map"""
        x, y = location
        if y < 0 or y >= len(self.layout):
            return False
        if x < 0 or x >= len(self.layout[y]):
            return False
        if self.layout[y][x] in [".", "#"]:
            return True
        return False

    def determine_face(self, location: tuple):
        """
        Determine which face 1-6 a given co-ordinate is on
        Returns 0 if out of bounds
            22221111
            22221111
            22221111
            3333
            3333
            3333
        55554444
        55554444
        55554444
        6666
        6666
        6666

        """
        x, y = location
        if 0 <= x < 50:
            if 100 <= y < 150:
                return 5
            if 150 <= y < 200:
                return 6
        if 50 <= x < 100:
            if 0 <= y < 50:
                return 2
            if 50 <= y < 100:
                return 3
            if 100 <= y < 150:
                return 4
        if 100 <= x < 150:
            if 0 <= y < 50:
                return 1
        return 0

    def get_direction_of_travel(self, from_location: tuple, to_location: tuple) -> str:
        """Infer direction of travel from two locations"""
        from_x, from_y = from_location
        to_x, to_y = to_location
        if from_x < to_x:
            return "R"
        if from_x > to_x:
            return "L"
        if from_y < to_y:
            return "D"
        # from_y>to_y
        return "U"

    def get_tentative_next_location(self, from_location: tuple, direction: str):
        """Return next set of valid-cordinates given cube wrapping"""
        from_x, from_y = from_location
        tentative_location = None
        match direction:
            case "R":
                tentative_location = (from_x + 1, from_y)
            case "L":
                tentative_location = (from_x - 1, from_y)
            case "U":
                tentative_location = (from_x, from_y - 1)
            case "D":
                tentative_location = (from_x, from_y + 1)
        return tentative_location

    def get_location_and_orientation(self, from_location: tuple, direction: str):
        """Returns genuine co-ordinates and orientation when moving one step in direction from location"""
        tentative_next_location = self.get_tentative_next_location(
            from_location, direction
        )
        if self.is_viable_location(tentative_next_location):
            return tentative_next_location, direction

        from_face = self.determine_face(from_location)
        x, y = from_location
        match from_face, direction:
            case 1, "U":
                return (x - 100, 199), "U"
            case 1, "D":
                return (99, x - 50), "L"
            case 1, "R":
                return (99, 149 - y), "L"
            case 2, "U":
                return (0, x + 100), "R"
            case 2, "L":
                return (0, 149 - y), "R"
            case 3, "L":
                return (y - 50, 100), "D"
            case 3, "R":
                return (y + 50, 49), "U"
            case 4, "D":
                return (49, x + 100), "L"
            case 4, "R":
                return (149, 149 - y), "L"
            case 5, "U":
                return (50, x + 50), "R"
            case 5, "L":
                return (50, 149 - y), "R"
            case 6, "D":
                return (x + 100, 0), "D"
            case 6, "L":
                return (y - 100, 0), "D"
            case 6, "R":
                return (y - 100, 149), "U"
        raise Exception("Unexcepted Combo")

    def get_new_orientation(self, from_location: tuple, to_location: tuple) -> str:
        """
        Returns new_orientation when moving
        Blank string means no change
        """
        from_face = self.determine_face(from_location)
        to_face = self.determine_face(to_location)
        if from_face == to_face:
            return ""

        direction = self.get_direction_of_travel(from_location, to_location)

        match from_face, direction:
            case 1, "R":
                return "L"
            case 1, "L":
                return "L"
            case 1, "D":
                return "L"
            case 1, "U":
                return "U"

            case 2, "R":
                return "R"
            case 2, "L":
                return "R"
            case 2, "D":
                return "D"
            case 2, "U":
                return "R"

            case 3, "R":
                return "U"
            case 3, "L":
                return "D"
            case 3, "D":
                return "D"
            case 3, "U":
                return "U"

            case 4, "R":
                return "L"
            case 4, "L":
                return "L"
            case 4, "D":
                return "L"
            case 4, "U":
                return "U"

            case 5, "R":
                return "R"
            case 5, "L":
                return "R"
            case 5, "D":
                return "D"
            case 5, "U":
                return "R"

            case 6, "R":
                return "U"
            case 6, "L":
                return "D"
            case 6, "D":
                return "D"
            case 6, "U":
                return "U"

    def get_square_content(self, location: tuple) -> str:
        """Returns content of square at given location, returns a blank space if out of range"""
        x, y = location
        if y < 0 or y >= len(self.layout):
            return " "
        if x < 0 or x >= len(self.layout[y]):
            return " "
        return self.layout[y][x]

    def get_next_location_and_direction(self, location: tuple, direction: str) -> tuple:
        """Return location of next valid square given a combination of valid and direction"""
        x, y = location
        match direction:
            case "R":
                new_x, new_y = x + 1, y
                if new_x >= len(self.layout[y]):
                    new_x = 0
                while self.get_square_content((new_x, new_y)) == " ":
                    new_x += 1
                    if new_x >= len(self.layout[y]):
                        new_x = 0
            case "L":
                new_x, new_y = x - 1, y
                if new_x < 0:
                    new_x = len(self.layout[y]) - 1
                while self.get_square_content((new_x, new_y)) == " ":
                    new_x -= 1
                    if new_x < 0:
                        new_x = len(self.layout[y]) - 1
            case "U":
                new_x, new_y = x, y - 1
                if new_y < 0:
                    new_y = len(self.layout) - 1
                while self.get_square_content((new_x, new_y)) == " ":
                    new_y -= 1
                    if new_y < 0:
                        new_y = len(self.layout) - 1
            case "D":
                new_x, new_y = x, y + 1
                if new_y > len(self.layout):
                    new_y = 0
                while self.get_square_content((new_x, new_y)) == " ":
                    new_y += 1
                    if new_y > len(self.layout):
                        new_y = 0
        return (new_x, new_y)
