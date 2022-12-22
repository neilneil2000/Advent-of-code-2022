from day_twenty_two_input import EXAMPLE_INPUT, PUZZLE_INPUT
from grove import Grove
from cube_grove import CubeGrove
from person import Walker


def parse_directions(directions: str) -> list:
    """CONVERT 10R56L1R7R3L15 to [10,R,56,L,1,R,7,R,3,L,15]"""
    index = 0
    parsed = []
    while index < len(directions):
        new_index_l = directions.find("L", index)
        new_index_r = directions.find("R", index)
        if new_index_l == -1 and new_index_r == -1:
            parsed.append(int(directions[index:]))
            break
        if new_index_l == -1:
            new_index = new_index_r
        elif new_index_r == -1:
            new_index = new_index_l
        else:
            new_index = min(new_index_l, new_index_r)
        parsed.append(int(directions[index:new_index]))
        parsed.append(directions[new_index])
        index = new_index + 1
    return parsed


def parse_input(input_string):
    return input_string.split("\n\n")[0].splitlines(), parse_directions(
        input_string.split("\n\n")[1]
    )


def main():
    layout, directions = parse_input(PUZZLE_INPUT)
    # starfruit_grove = Grove(layout)
    # me = Walker(starfruit_grove, directions)
    # me.follow_directions()
    # print(me.password())

    starfruit_cube = CubeGrove(layout)
    me_two = Walker(starfruit_cube, directions)
    me_two.follow_directions()
    print(me_two.password())


if __name__ == "__main__":
    main()
