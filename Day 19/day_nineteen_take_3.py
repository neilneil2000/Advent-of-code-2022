from functools import lru_cache
from time import perf_counter

from day_nineteen_input import EXAMPLE_INPUT, PUZZLE_INPUT


class Game:
    def __init__(self, index: int, blueprint: dict, game_time: int = 24) -> None:
        self.game_time = game_time
        self.index = index
        self.costs = blueprint
        self.maxima = {
            "ore": max(self.costs[x]["ore"] for x in self.costs),
            "clay": self.costs["obsidian"]["clay"],
            "obsidian": self.costs["geode"]["obsidian"],
        }
        print(f"Game {self.index} created:")
        print(f"Blueprint: {self.costs}")
        print(
            f"Maximums: Ore-{self.maxima['ore']}, Clay-{self.maxima['clay']}, Obsidian-{self.maxima['obsidian']}"
        )

    def collect(self, resources: dict, robots: dict):
        """Update resources"""
        for resource in resources:
            resources[resource] += robots[resource]

    def build_robot(self, resources: dict, robots: dict, robot_type: str):
        """Build a robot of robot_type"""
        if robots[robot_type] >= self.maxima[robot_type]:
            return False  # Don't bother going over maximum useful
        for resource in self.costs[robot_type]:
            resources[resource] -= self.costs[robot_type][resource]
        robots[robot_type] += 1
        for resource_amount in resources.values():
            if resource_amount < 0:
                return False
        return True

    def update_resources(self, resources: dict, robots: dict, robot_to_build: str):
        EMPTY_RESOURCE = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
        match robot_to_build:
            case "ore" | "clay" | "obsidian" | "geode":
                max_robots = self.maxima.get(robot_to_build)
                if max_robots is not None and max_robots <= robots[robot_to_build]:
                    return EMPTY_RESOURCE, EMPTY_RESOURCE
                for resource in self.costs[robot_to_build]:
                    new_value = (
                        resources[resource] - self.costs[robot_to_build][resource]
                    )
                    if new_value < 0:
                        return EMPTY_RESOURCE, EMPTY_RESOURCE
                    resources[resource] = new_value
                self.collect(resources, robots)
                robots[robot_to_build] += 1
            case _:
                self.collect(resources, robots)

        return resources, robots

    @staticmethod
    def is_subset(
        resource_candidate: dict, robot_candidate: dict, resources: list, robots: list
    ):
        """Returns True if resource and robot option are subset of one of resource,robots list entries"""
        for index, _ in enumerate(resources):
            subset = True
            for resource_type in ["ore", "clay", "obsidian", "geode"]:
                if resource_candidate[resource_type] > resources[index][resource_type]:
                    subset = False
                    break
                if robot_candidate[resource_type] > robots[index][resource_type]:
                    subset = False
                    break
            if subset:
                return True

        return False

    def is_affordable(self, resources, robot_type):
        """Returns True if robot_type is affordable with resources"""
        if robot_type == "save":
            return True
        for resource in self.costs[robot_type]:
            if self.costs[robot_type][resource] > resources[resource]:
                return False
        return True

    @staticmethod
    def include_into_options(
        resource_candidate: dict, robot_candidate: dict, resources: list, robots: list
    ):
        removal_list = []
        for index, _ in enumerate(resources):
            robot_comparator = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
            resource_comparator = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
            for resource_type in ["ore", "clay", "obsidian", "geode"]:
                robot_comparator[resource_type] = (
                    robot_candidate[resource_type] - robots[index][resource_type]
                )
                resource_comparator[resource_type] = (
                    resource_candidate[resource_type] - resources[index][resource_type]
                )
            if all(value <= 0 for value in robot_comparator.values()) and all(
                value <= 0 for value in resource_comparator.values()
            ):
                if removal_list:
                    raise Exception("Shouldn't Happen")
                return
            if all(value >= 0 for value in robot_comparator.values()) and all(
                value >= 0 for value in resource_comparator.values()
            ):
                removal_list.append(index)
        for index in sorted(removal_list, reverse=True):
            robots.pop(index)
            resources.pop(index)
        robots.append(robot_candidate)
        resources.append(resource_candidate)

    @staticmethod
    @lru_cache
    def get_build_options(time_left):
        if time_left == 2:
            return ["geode"]
        return ["ore", "clay", "obsidian", "geode"]

    def take_turn(
        self,
        resources: list,
        robots: list,
        time_left: int,
    ):
        """Execute a single 1 minute round of the game"""
        print(
            f"{time_left} Minutes left - {len(resources)} potential cases to consider"
        )
        if time_left == 1:
            geodes = 0
            for resource_entry, robot_entry in zip(resources, robots):
                geodes = max(geodes, resource_entry["geode"] + robot_entry["geode"])
            return geodes
        new_resources = []
        new_robots = []
        for resource_option, robot_option in zip(resources, robots):
            option_count = 0
            for action in self.get_build_options(time_left):
                if not self.is_affordable(resource_option, action):
                    continue
                resource_result, robot_result = self.update_resources(
                    resource_option.copy(), robot_option.copy(), action
                )
                self.include_into_options(
                    resource_result, robot_result, new_resources, new_robots
                )
                option_count += 1
            if (
                option_count > 0 and robot_option["ore"] >= self.maxima["ore"]
            ) or robot_option["ore"] + resource_option["ore"] >= 2 * self.maxima["ore"]:
                continue  # Don't bother saving if I will have enough anyway
            resource_result, robot_result = self.update_resources(
                resource_option.copy(), robot_option.copy(), "save"
            )
            self.include_into_options(
                resource_result, robot_result, new_resources, new_robots
            )

        return self.take_turn(new_resources, new_robots, time_left - 1)

    def run_game(self) -> int:
        """Return Maximum number of geodes that can be harvested in a game"""
        initial_resources = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
        initial_robots = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}
        initial_time = self.game_time
        return self.take_turn([initial_resources], [initial_robots], initial_time)

    def get_quality_score(self):
        """Return Quality Score as defined in problem statement"""
        maximum_geodes = self.run_game()
        print(f"Maximum Geodes: {maximum_geodes}")
        return self.index * maximum_geodes


def parse_input(puzzle_input: str):
    """Return dict of ID:Resource_costs"""
    robot_costs = {}
    for line in puzzle_input.splitlines():
        # Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
        line = line.split()
        index = int(line[1][:-1])
        ore_cost = int(line[6])
        clay_cost = int(line[12])
        obsidian_cost_ore = int(line[18])
        obisidian_cost_clay = int(line[21])
        geode_cost_ore = int(line[27])
        geode_cost_obsidian = int(line[30])
        robot_costs[index] = {
            "ore": {"ore": ore_cost},
            "clay": {"ore": clay_cost},
            "obsidian": {"ore": obsidian_cost_ore, "clay": obisidian_cost_clay},
            "geode": {"ore": geode_cost_ore, "obsidian": geode_cost_obsidian},
        }
    return robot_costs


def main():  # pylint:disable=missing-function-docstring
    blueprints = parse_input(EXAMPLE_INPUT)
    total = 0
    for index, blueprint in blueprints.items():
        start = perf_counter()
        total += Game(index, blueprint, 24).get_quality_score()
        end = perf_counter()
        print(f"Blueprint {index} assessed in {end-start}")
    print(total)

    # for index, blueprint in blueprints.items():
    #     if index == 4:
    #         break
    #     start = perf_counter()
    #     total *= Game(index, blueprint, 32).run_game()
    #     end = perf_counter()
    #     print(f"Blueprint {index} assessed in {end-start}")
    # print(total)


if __name__ == "__main__":
    main()
