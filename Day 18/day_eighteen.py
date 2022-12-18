"""Advent of Code 2022 Day 18 Solution"""
from day_eighteen_input import EXAMPLE_INPUT, PUZZLE_INPUT


def get_neighbours(location: tuple) -> set:
    """Return set of all neighbouring locations"""
    x, y, z = location
    neighbours = set()
    if x > -1:
        neighbours.add((x - 1, y, z))
    if x < 23:
        neighbours.add((x + 1, y, z))
    if y > -1:
        neighbours.add((x, y - 1, z))
    if y < 23:
        neighbours.add((x, y + 1, z))
    if z > -1:
        neighbours.add((x, y, z - 1))
    if z < 23:
        neighbours.add((x, y, z + 1))
    return neighbours


def process_input(input_string: str) -> set:
    cubes = set()
    for entry in input_string.splitlines():
        x, y, z = entry.split(",")
        cubes.add((int(x), int(y), int(z)))
    return cubes


def get_boundary_cubes() -> set:
    """Return set of cubes known to be on the outside"""
    lower_limit = 0  # inclusive
    upper_limit = 21  # inclusive

    boundary_cubes = set()
    for i in range(lower_limit - 1, upper_limit + 2):
        for j in range(lower_limit - 1, upper_limit + 2):
            boundary_cubes.add((lower_limit - 1, i, j))
            boundary_cubes.add((upper_limit + 2, i, j))
            boundary_cubes.add((i, lower_limit - 1, j))
            boundary_cubes.add((i, upper_limit + 2, j))
            boundary_cubes.add((i, j, lower_limit - 1))
            boundary_cubes.add((i, j, upper_limit + 2))
    return boundary_cubes


def find_neighbours_in_set(cube_of_interest, set_of_cubes):
    """Returns subset of 'set_of_cubes' which are neighbours of 'cube_of_interest'"""
    neighbours = get_neighbours(cube_of_interest)
    return neighbours.intersection(set_of_cubes)


def recursive_loop(current_set, cubes, current_cube):
    neighbours = find_neighbours_in_set(current_cube, cubes)
    current_set.update(neighbours)
    cubes.difference_update(neighbours)
    for neighbour in neighbours:
        recursive_loop(current_set, cubes, neighbour)


def break_into_sets(cubes: set):
    """Return list of sets where each set is a contiguous space"""
    cube_sets = []
    while cubes:
        current_cube = cubes.pop()
        current_set = {current_cube}
        recursive_loop(current_set, cubes, current_cube)
        cube_sets.append(current_set)
    return cube_sets


def get_playing_area():
    playing_cubes = set()
    for x in range(-1, 23):
        for y in range(-1, 23):
            for z in range(-1, 23):
                playing_cubes.add((x, y, z))
    return playing_cubes


def get_surface_area(cube_set):
    blocked_faces = 0
    for cube in cube_set:
        for neighbour in get_neighbours(cube):
            if neighbour in cube_set:
                blocked_faces += 1
    return (6 * len(cube_set)) - blocked_faces


def main():  # pylint:disable=missing-function-docstring
    lava_cubes = process_input(PUZZLE_INPUT)

    # Part 1
    total_surface_area = get_surface_area(lava_cubes)
    print(f"Total Surface Area = {total_surface_area}")

    # Part 2
    outside_cubes = get_boundary_cubes()
    checking_outside_cubes = outside_cubes.copy()
    while checking_outside_cubes:
        new_air_cubes = set()
        for air_cube in checking_outside_cubes:
            for possible_cube in get_neighbours(air_cube):
                if possible_cube in lava_cubes or possible_cube in outside_cubes:
                    continue
                new_air_cubes.add(possible_cube)
        outside_cubes.update(new_air_cubes)
        checking_outside_cubes = new_air_cubes.copy()

    print(f"Total Playing area = 25^3={25**3}")
    print(f"Total Outside cubes = {len(outside_cubes)}")
    print(f"Total Lava + Air cubes = {25**3-len(outside_cubes)}")
    print(f"Total Lava cubes = {len(lava_cubes)}")
    print(f"Total trapped air cubes = {25**3-len(outside_cubes)-len(lava_cubes)}")
    playing_area = get_playing_area()
    total_cubes = outside_cubes.union(lava_cubes)
    trapped_air_cubes = playing_area.difference(total_cubes)
    # print(trapped_air_cubes)
    print(f"Total trapped air cubes confirmed as {len(trapped_air_cubes)}")
    cube_sets = break_into_sets(trapped_air_cubes.copy())
    internal_surface_area = 0
    for cube_set in cube_sets:
        internal_surface_area += get_surface_area(cube_set)
    print(f"Internal Surface Area = {internal_surface_area}")
    print(
        f"External Surface Area = {total_surface_area} - {internal_surface_area} = {total_surface_area-internal_surface_area}"
    )


if __name__ == "__main__":
    main()
