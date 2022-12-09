from day_nine_input import PUZZLE_INPUT


class Rope:
    """Model of a simple rope with 2 ends"""

    def __init__(self):
        self.head = (0, 0)
        self.tail_history = [(0, 0)]

    @property
    def tail(self):
        return self.tail_history[-1]

    def unique_tail_locations(self):
        return len(set(self.tail_history))

    def move_head(self, direction: str):
        x, y = self.head
        match direction:
            case "U":  # up
                self.head = (x, y + 1)
            case "D":  # down
                self.head = (x, y - 1)
            case "R":  # right
                self.head = (x + 1, y)
            case "L":  # left
                self.head = (x - 1, y)

    def move_tail(self):
        head_x, head_y = self.head
        tail_x, tail_y = self.tail

        x_displacement = abs(head_x - tail_x)
        y_displacement = abs(head_y - tail_y)

        if x_displacement <= 1 and y_displacement <= 1:
            return
        if x_displacement > 1 and y_displacement == 0:
            new_x = (head_x + tail_x) // 2
            self.tail_history.append((new_x, tail_y))
            return
        if x_displacement == 0 and y_displacement > 1:
            new_y = (head_y + tail_y) // 2
            self.tail_history.append((tail_x, new_y))
            return
        if x_displacement > 1:  # and y=1
            new_x = (head_x + tail_x) // 2
            self.tail_history.append((new_x, head_y))
            return
        if y_displacement > 1:  # and x=1
            new_y = (head_y + tail_y) // 2
            self.tail_history.append((head_x, new_y))

    def command(self, direction: str, steps: int):
        for _ in range(steps):
            self.move_head(direction)
            self.move_tail()


def main():
    rows = PUZZLE_INPUT.splitlines()
    rope = Rope()
    for row in rows:
        direction, steps = row.split()
        rope.command(direction, int(steps))
    print(rope.unique_tail_locations())


if __name__ == "__main__":
    main()
