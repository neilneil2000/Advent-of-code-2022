from day_fourteen_input import EXAMPLE_INPUT, PUZZLE_INPUT


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
    """Returns list of rock positions"""
    rocks = set()
    starting_rock = rock_lines.pop(0)
    for rock_end in rock_lines:
        rocks = rocks.union(get_rocks_in_line(starting_rock, rock_end))
        starting_rock = rock_end
    return rocks


def is_in_abyss(position):
    MAXIMUM_DEPTH = 166
    _, y = position
    return y > MAXIMUM_DEPTH


def get_landing_place(sand_position: tuple, objects: set):
    if is_in_abyss(sand_position):
        return (-1, -1)
    x, y = sand_position
    directly_below = (x, y + 1)
    if directly_below not in objects:
        return get_landing_place(directly_below, objects)
    down_left = (x - 1, y + 1)
    if down_left not in objects:
        return get_landing_place(down_left, objects)
    down_right = (x + 1, y + 1)
    if down_right not in objects:
        return get_landing_place(down_right, objects)
    return sand_position


def get_landing_place_with_floor(sand_position: tuple, objects: set, floor_level: int):
    x, y = sand_position
    if y == floor_level - 1:
        return sand_position
    directly_below = (x, y + 1)
    if directly_below not in objects:
        return get_landing_place_with_floor(directly_below, objects, floor_level)
    down_left = (x - 1, y + 1)
    if down_left not in objects:
        return get_landing_place_with_floor(down_left, objects, floor_level)
    down_right = (x + 1, y + 1)
    if down_right not in objects:
        return get_landing_place_with_floor(down_right, objects, floor_level)
    return sand_position


def lowest_rock_position(rocks):
    lowest = 0
    for rock in rocks:
        _, y = rock
        lowest = max(lowest, y)
    return lowest


def main():  # pylint:disable=missing-function-docstring
    puzzle = [line.split(" -> ") for line in PUZZLE_INPUT.splitlines()]
    rocks = set()
    for rock_formation in puzzle:
        line = [tuple(map(int, x.split(","))) for x in rock_formation]
        # print(line)
        rocks = rocks.union(get_rock_positions(line))
    # print(rocks)
    floor_level = lowest_rock_position(rocks) + 2
    landing_position = (0, 0)
    sand = set()
    while landing_position != (500, 0):
        landing_position = get_landing_place_with_floor(
            (500, 0), rocks.union(sand), floor_level
        )
        sand.add(landing_position)
    print(len(sand))

    floor_level = 168


if __name__ == "__main__":
    main()
