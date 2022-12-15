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
    return abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])


def ruled_out_points_on_line(
    y_co_ordinate: int, point: tuple, beacon_distance: int
) -> tuple:
    """Returns tuple of start and finish x co-ordinates along line described by y_co_ordinate where a beacon CANNOT exist"""
    x, y = point
    black_spots = ()
    distance = abs(y - y_co_ordinate)
    overlap = beacon_distance - distance
    if overlap < 0:
        return black_spots
    return (x - overlap, x + overlap)


def find_gap(tuple_range: dict, range_start: int, range_end: int):
    """Returns co-ordinate of gap in a range or None if contiguous"""
    if range_start < min(tuple_range):
        return range_start
    if range_end > max(tuple_range.values()):
        return range_end
    pointer = range_start
    for start in sorted(tuple_range):
        if start > pointer + 1:
            return pointer + 1
        pointer = max(pointer, tuple_range[start])
    return None


def add_range_to_dictionary(dictionary: dict, new_range: tuple):
    """Adds new_range to dictionary"""
    start, end = new_range
    if dictionary.get(start):
        dictionary[start] = max(dictionary[start], end)
    else:
        dictionary[start] = end
    return dictionary


def compute_tuning_frequency(x_coordinate: int, y_coordinate: int):
    return 4_000_000 * x_coordinate + y_coordinate


def main():

    sensors = process_input(PUZZLE_INPUT)
    beacons = set(sensors.values())
    print("Input Processed")
    for line in range(0, 4_000_001):
        line_black_spots = {}
        for sensor, beacon in sensors.items():
            sensor_distance = manhattan_distance(sensor, beacon)
            sensor_black_spots = ruled_out_points_on_line(line, sensor, sensor_distance)
            if sensor_black_spots:
                line_black_spots = add_range_to_dictionary(
                    line_black_spots, sensor_black_spots
                )
        gap = find_gap(line_black_spots, 0, 4_000_001)
        if not line % 100_000:
            print(f"Line {line} Assessed")
        if gap is not None:
            break

    print(f"x={gap}, y={line}")
    print(f"Tuning Frequency is: {compute_tuning_frequency(gap, line)}")

    """ sensors = process_input(EXAMPLE_INPUT)
    beacons = set(sensors.values())
    black_spots = []
    line_of_focus = 10
    for sensor, beacon in sensors.items():
        line_black_spots = ruled_out_points_on_line_optimised(
            line_of_focus, sensor, manhattan_distance(sensor, beacon)
        )
        black_spots = merge_ranges(black_spots, line_black_spots)

    for beacon in beacons:
        x, y = beacon
        if y == line_of_focus:
            black_spots.discard(x)
            print(f"Removed {x}")
    print(len(black_spots))
    ideal_set = set(range(0, 4_000_001))
    pass
    for line_of_focus in range(0, 4_000_001):
        for sensor, beacon in sensors.items():
            black_spots.update(
                ruled_out_points_on_line(
                    line_of_focus, sensor, manhattan_distance(sensor, beacon)
                )
            )
        print(f"Row {line_of_focus} Complete")
        if ideal_set - black_spots:
            break
    pass
 """


if __name__ == "__main__":
    main()
