"""Advent of Code 2022 Day 15 Solution"""
from functools import lru_cache
from day_fifteen_input import EXAMPLE_INPUT, PUZZLE_INPUT


def process_input(input_string: str) -> list:
    """Convert input string into list of entries"""
    processed = {}
    entries = input_string.splitlines()
    for entry in entries:
        entry = entry.split("=")
        processed[(int(entry[1].split(",")[0]), int(entry[2].split(":")[0]))] = (
            int(entry[3].split(",")[0]),
            int(entry[4]),
        )
    return processed


@lru_cache
def manhattan_distance(point_a, point_b):
    """Returns Manhattan distance between 2 points"""
    return abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])


def ruled_out_points_on_line(y_co_ordinate: int, sensor: tuple, beacon: tuple) -> tuple:
    """Returns tuple of start and finish x co-ordinates along line described by y_co_ordinate where a beacon CANNOT exist"""
    x, y = sensor  # pylint:disable=invalid-name
    beacon_distance = manhattan_distance(sensor, beacon)
    black_spots = ()
    distance = abs(y - y_co_ordinate)
    overlap = beacon_distance - distance
    if overlap < 0:
        return black_spots
    return (x - overlap, x + overlap)


def find_gap(number_line: dict, range_start: int, range_end: int):
    """Returns first gap in a range or None if contiguous"""
    if range_start < min(number_line):
        return range_start
    if range_end > max(number_line.values()):
        return range_end
    pointer = range_start
    for start in sorted(number_line):
        if start > pointer + 1:
            return pointer + 1
        pointer = max(pointer, number_line[start])
    return None


def count_blocks(number_line: dict):
    """number of blocks covered by number line"""
    lowest = min(number_line)
    highest = max(number_line.values())
    missing = 0
    pointer = lowest
    for start in sorted(number_line):
        gap = start - pointer - 1
        if gap > 0:
            missing += gap
            pointer += gap
        else:
            pointer = max(pointer, number_line[start])
    return highest - lowest - missing


def add_range_to_dictionary(dictionary: dict, new_range: tuple):
    """Adds new_range to dictionary"""
    start, end = new_range
    if dictionary.get(start):
        dictionary[start] = max(dictionary[start], end)
    else:
        dictionary[start] = end
    return dictionary


def compute_tuning_frequency(x_coordinate: int, y_coordinate: int):
    """Calculate the Tuning Frequency as described in part 2 of the puzzle"""
    return 4_000_000 * x_coordinate + y_coordinate


def main():  # pylint:disable=missing-function-docstring

    sensors = process_input(PUZZLE_INPUT)
    part_one_row = 2_000_000
    part_two_limit = 4_000_000
    part_one_black_spots = {}
    gap = None
    print("Input Processed")
    print("Assessing Lines...")
    for line in range(0, part_two_limit + 1):
        line_black_spots = {}
        for sensor, beacon in sensors.items():
            sensor_black_spots = ruled_out_points_on_line(line, sensor, beacon)
            if sensor_black_spots:
                line_black_spots = add_range_to_dictionary(
                    line_black_spots, sensor_black_spots
                )
        if line == part_one_row:
            part_one_black_spots = line_black_spots
        gap = find_gap(line_black_spots, 0, part_two_limit + 1)
        if gap is not None:
            print(f"{line} Lines Assessed")
            break
        if not line % 100_000:
            print(f"{line} Lines Assessed", end="\r")

    print(count_blocks(part_one_black_spots))
    print(f"x={gap}, y={line}")
    print(f"Tuning Frequency is: {compute_tuning_frequency(gap, line)}")


if __name__ == "__main__":
    main()
