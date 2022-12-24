from day_twenty_four_input import EXAMPLE_INPUT, PUZZLE_INPUT, EXAMPLE_INPUT_2


def parse_input(input_multiline: str):
    parsed = {"<": set(), ">": set(), "^": set(), "v": set()}
    width = None
    for y, line in enumerate(input_multiline.splitlines()):
        line = line.strip("#")
        if len(line) == 1:
            if parsed.get("start") is None:
                parsed["start"] = (0, y - 1)
            else:
                parsed["end"] = (width - 1, y - 1)
        else:
            if parsed.get("width") is None:
                width = len(line)
                parsed["width"] = width
            for x, character in enumerate(line):
                if character == ".":
                    continue
                parsed[character].add((x, y - 1))
    parsed["height"] = y - 1
    return parsed


class Valley:
    def __init__(self, positions: dict) -> None:
        self.start = positions["start"]
        self.end = positions["end"]
        self.width = positions["width"]
        self.height = positions["height"]
        self.blizzards = {}
        for direction in ["<", ">", "^", "v"]:
            self.blizzards[direction] = positions[direction]
        self.possible_positions = {self.start}
        self.moves = 0

    def move_blizzards(self) -> None:
        new_blizzards = {"<": set(), ">": set(), "^": set(), "v": set()}
        for left_blizzard in self.blizzards["<"]:
            x, y = left_blizzard
            new_blizzards["<"].add(((x - 1) % self.width, y))
        for right_blizzard in self.blizzards[">"]:
            x, y = right_blizzard
            new_blizzards[">"].add(((x + 1) % self.width, y))
        for up_blizzard in self.blizzards["^"]:
            x, y = up_blizzard
            new_blizzards["^"].add((x, (y - 1) % self.height))
        for down_blizzard in self.blizzards["v"]:
            x, y = down_blizzard
            new_blizzards["v"].add((x, (y + 1) % self.height))
        self.blizzards = new_blizzards

    def get_possible_places(self, current_position) -> set():
        """Return set of places I could move to (including where I am now)"""
        x, y = current_position
        possible_places = {
            (x - 1, y),
            (x, y - 1),
            (x, y),
            (x, y + 1),
            (x + 1, y),
        }
        if self.end in possible_places:
            return {self.end}  # If you can get out, get out!
        possible_places.difference_update(self.blizzards["<"])
        possible_places.difference_update(self.blizzards[">"])
        possible_places.difference_update(self.blizzards["^"])
        possible_places.difference_update(self.blizzards["v"])
        confirmed_places = set()
        for place in possible_places:
            if place == self.start:
                confirmed_places.add(place)
                continue
            x, y = place
            if 0 <= x < self.width and 0 <= y < self.height:
                confirmed_places.add(place)
        return confirmed_places

    def display_valley(self):
        for y in range(-1, self.height + 1):
            if y == -1 or y == self.height:
                row = "#" * (self.width + 2)
                print(row)
                continue
            row = "#"
            for x in range(0, self.width):
                count = 0
                character = "."
                if (x, y) in self.blizzards["<"]:
                    count += 1
                    character = "<"
                if (x, y) in self.blizzards[">"]:
                    count += 1
                    character = ">"
                if (x, y) in self.blizzards["^"]:
                    count += 1
                    character = "^"
                if (x, y) in self.blizzards["v"]:
                    count += 1
                    character = "v"
                if count > 1:
                    row += str(count)
                else:
                    row += character
            print(row + "#")
        print()

    def update_safe_positions(self):
        new_positions = set()
        for position in self.possible_positions:
            new_positions.update(self.get_possible_places(position))
        self.possible_positions = new_positions
        # print(self.possible_positions)

    def execute_move(self):
        self.move_blizzards()
        self.update_safe_positions()
        self.moves += 1

    def switch_start_and_end(self):
        old_end = self.end
        old_start = self.start
        self.start = old_end
        self.end = old_start

    def there_and_back_and_back_again(self):
        self.display_valley()
        while True:
            self.execute_move()
            if self.end in self.possible_positions:
                break
        self.switch_start_and_end()
        self.possible_positions = {self.start}
        while True:
            self.execute_move()
            if self.end in self.possible_positions:
                break
        self.switch_start_and_end()
        self.possible_positions = {self.start}
        while True:
            self.execute_move()
            if self.end in self.possible_positions:
                return self.moves

    def go_to_end(self):
        # self.display_valley()
        while True:
            self.execute_move()
            if self.end in self.possible_positions:
                return self.moves


def main():
    puzzle = parse_input(PUZZLE_INPUT)
    blizzard_valley = Valley(puzzle)
    moves = blizzard_valley.go_to_end()
    print(f"Reached end in {moves} moves")

    blizzard_valley_2 = Valley(puzzle)
    moves = blizzard_valley_2.there_and_back_and_back_again()
    print(f"Reached end in {moves} moves")


if __name__ == "__main__":
    main()
