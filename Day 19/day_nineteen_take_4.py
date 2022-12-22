from functools import lru_cache
from time import perf_counter

from day_nineteen_input import EXAMPLE_INPUT, PUZZLE_INPUT


class SimpleTree:
    def __init__(self):
        self.paths = {1: {0, 2}, 2: {1, 5}}  # robots:ore
        self.cost = 2

    def get_incremented(self):
        new_paths = {}
        for robots, ore_down in self.paths.items():
            new_paths[robots] = set()
            for ore in ore_down:
                new_paths[robots].add(ore + robots)
        self.paths = new_paths

    def buy_robot(self):
        new_paths = {}
        for robots, ore_down in self.paths.items():
            new_paths[robots + 1] = set()
            for ore in ore_down:
                if ore >= self.cost:  # Buy one
                    new_paths[robots + 1].add(ore - self.cost)
        self.paths = new_paths

    def play_round(self):
        new_paths = {}
        for robots, ore_down in self.paths.items():
            if new_paths.get(robots) is None:
                new_paths[robots] = set()
            if new_paths.get(robots + 1) is None:
                new_paths[robots + 1] = set()
            for ore in ore_down:
                new_paths[robots].add(ore + robots)
                if ore >= self.cost:  # Buy one
                    new_paths[robots + 1].add(ore - self.cost + robots)
        self.paths = new_paths


class DoubleTree:
    def __init__(self):
        self.paths = {2: {1: {1: {0, 2}, 2: {1, 5}}}}  # robots:ore:robots:ore
        self.ore_robot_cost = 2
        self.geode_robot_cost = 4

    def play_round(self):
        new_paths = {}
        for geode_robots, geodes_down in self.paths.items():
            if new_paths.get(geode_robots) is None:
                new_paths[geode_robots] = set()
            if new_paths.get(geode_robots + 1) is None:
                new_paths[geode_robots + 1] = set()
            for geodes, ore_robots_down in geodes_down.items():
                for ore_robots, ore_down in ore_robots_down.items():
                    if new_paths.get(ore_robots) is None:
                        new_paths[ore_robots] = set()
                    if new_paths.get(ore_robots + 1) is None:
                        new_paths[ore_robots + 1] = set()
                    for ore in ore_down:
                        new_paths[ore_robots].add(ore + ore_robots)
                        if ore >= self.ore_robot_cost:  # Buy one
                            new_paths[ore_robots + 1].add(
                                ore - self.ore_robot_cost + ore_robots
                            )
        self.paths = new_paths


class StateTree:
    """
    CONCEPT OF STATE OPTIONS TREE

    open_paths = {0:{0:{0:{0:{0:{0:{0:{0:0}}}}}}}}
    geodes:geode_robots:ore:ore_robots:clay:clay_robots:obsidian:obsidian_robots
    open_paths = {0: {},1:{}}

    """

    def __init__(self):
        self.paths = {0: {0: {1: {0: {0: {0: {0: {0: 0}}}}}}}}

    def get_incremented(self) -> dict:
        """Return option tree with all increments"""
        new_paths = {}
        for geode_robots, geodes_down in self.paths.items():
            for geodes, ore_robots_down in geodes_down.items():
                for ore_robots, ore_down in ore_robots_down.items():
                    for ore, clay_robots_down in ore_down.items():
                        for clay_robots, clay_down in clay_robots_down.items():
                            for clay, obsidian_robots_down in clay_down.items():
                                for (
                                    obsidian_robots,
                                    obsidian,
                                ) in obsidian_robots_down.items():
                                    new_paths[geode_robots][geodes][ore_robots][ore][
                                        clay_robots
                                    ][clay][obsidian_robots][obsidian] = (
                                        geodes + geode_robots
                                    )


def main():  # pylint:disable=missing-function-docstring
    new_tree = DoubleTree()
    new_tree.play_round()


if __name__ == "__main__":
    main()
