from day_twenty_three_input import EXAMPLE_INPUT, PUZZLE_INPUT, SIMPLE_EXAMPLE


class PlantingArea:
    def __init__(self, layout: list) -> None:
        self.initial_layout = layout
        self.elf_locations = set()
        self.setup_elf_locations()
        self.consideration_order = ["N", "S", "W", "E"]

    def update_consideration_order(self) -> None:
        """Update order of directions to consider moving"""
        self.consideration_order.insert(4, self.consideration_order.pop(0))

    def setup_elf_locations(self) -> None:
        for y, row in enumerate(self.initial_layout):
            for x, character in enumerate(row):
                if character == "#":
                    self.elf_locations.add((x, y))

    def get_direction_coords(self, direction: str, elf: tuple) -> tuple:
        x, y = elf
        match direction:
            case "N":
                return {(x - 1, y - 1), (x, y - 1), (x + 1, y - 1)}
            case "S":
                return {(x - 1, y + 1), (x, y + 1), (x + 1, y + 1)}
            case "W":
                return {(x - 1, y - 1), (x - 1, y), (x - 1, y + 1)}
            case "E":
                return {(x + 1, y - 1), (x + 1, y), (x + 1, y + 1)}
            case _:
                raise ValueError("Direction not valid")

    def direction_possible(self, direction: str, elf: tuple) -> bool:
        """Returns True if possible for elf to move in direction"""
        new_spaces = self.get_direction_coords(direction, elf)
        if self.elf_locations.isdisjoint(new_spaces):
            return True
        return False

    def propose_move_in_direction(self, direction: str, elf: tuple) -> tuple:
        """Return location of new proposed position"""
        x, y = elf
        match direction:
            case "N":
                return (x, y - 1)
            case "S":
                return (x, y + 1)
            case "W":
                return (x - 1, y)
            case "E":
                return (x + 1, y)
            case _:
                raise ValueError("Direction not valid")

    def get_proposed_destination(self, elf: tuple):
        """Return proposed next space for elf to move to"""
        possible_directions = []
        for direction in self.consideration_order:
            if self.direction_possible(direction, elf):
                possible_directions.append(direction)

        if len(possible_directions) in [0, 4]:
            return elf
        return self.propose_move_in_direction(possible_directions[0], elf)

    @staticmethod
    def fix_clashes(proposed_elf_moves: dict) -> dict:
        """Find all expected clashes a set those elves to stay still"""
        confirmed_elf_moves = {}
        for destination, sources in proposed_elf_moves.items():
            if len(sources) == 1:
                confirmed_elf_moves[destination] = sources[0]
                continue
            for source in sources:
                confirmed_elf_moves[source] = source
        return confirmed_elf_moves

    def get_new_elf_locations(self) -> set:
        """Plan Moves for next round"""
        proposed_elf_moves = {}  # {dest:source}
        for source in self.elf_locations:
            destination = self.get_proposed_destination(source)
            if proposed_elf_moves.get(destination) is None:
                proposed_elf_moves[destination] = [source]
            else:
                proposed_elf_moves[destination].append(source)
        confirmed_elf_moves = self.fix_clashes(proposed_elf_moves)
        return set(confirmed_elf_moves.keys())

    def go(self):
        """Execute"""
        new_locations = self.get_new_elf_locations()
        self.print_grove(new_locations)
        rounds = 0
        while new_locations != self.elf_locations and rounds < 1000:
            self.elf_locations = new_locations
            self.update_consideration_order()
            new_locations = self.get_new_elf_locations()
            # self.print_grove(new_locations)
            rounds += 1
            print(f"Round {rounds} Completed", end="\r")
        print(f"Total Rounds: {rounds}")
        return rounds + 1

    @property
    def playing_area(self) -> int:
        """Return Area of field containing all elves"""
        min_x = min(elf_x for elf_x, _ in self.elf_locations)
        min_y = min(elf_y for _, elf_y in self.elf_locations)
        max_x = max(elf_x for elf_x, _ in self.elf_locations)
        max_y = max(elf_y for _, elf_y in self.elf_locations)

        return ((max_x - min_x) + 1) * ((max_y - min_y) + 1)

    @property
    def number_of_elves(self) -> int:
        """Return number of elves in play"""
        return len(self.elf_locations)

    def print_grove(self, locations: set = None):
        if locations == None:
            locations = self.elf_locations
        min_x = min(elf_x for elf_x, _ in locations)
        min_y = min(elf_y for _, elf_y in locations)
        max_x = max(elf_x for elf_x, _ in locations)
        max_y = max(elf_y for _, elf_y in locations)

        for y in range(min_y, max_y + 1):
            new_line = ""
            for x in range(min_x, max_x + 1):
                if (x, y) in locations:
                    new_line += "#"
                else:
                    new_line += "."
            print(new_line)
        print()


def main():  # pylint:disable=missing-function-docstring
    ash_grove = PlantingArea(PUZZLE_INPUT.splitlines())
    ash_grove.print_grove()
    print(ash_grove.go())
    area = ash_grove.playing_area
    elves = ash_grove.number_of_elves
    print(area - elves)


if __name__ == "__main__":
    main()
