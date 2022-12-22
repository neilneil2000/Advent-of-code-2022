class Grove:
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

    def get_square_content(self, location: tuple) -> str:
        """Returns content of square at given location, returns a blank space if out of range"""
        x, y = location
        if y < 0 or y >= len(self.layout):
            return " "
        if x < 0 or x >= len(self.layout[y]):
            return " "
        return self.layout[y][x]

    def get_next_location(self, location: tuple, direction: str) -> tuple:
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
