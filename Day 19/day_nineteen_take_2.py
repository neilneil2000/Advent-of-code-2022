from functools import lru_cache
from time import perf_counter

from day_nineteen_input import EXAMPLE_INPUT, PUZZLE_INPUT


class Game:
    def __init__(self, index: int, blueprint: dict, game_time: int = 24) -> None:
        self.game_time = game_time
        self.index = index
        self.costs = blueprint
        self.maximum_rates = {
            "ore": max(self.costs[x]["ore"] for x in self.costs),
            "clay": self.costs["obsidian"]["clay"],
            "obsidian": self.costs["geode"]["obsidian"],
            "geode": 1000,
        }
        print(f"Game {self.index} created:")
        print(f"Blueprint: {self.costs}")
        print(
            f"Maximums: Ore-{self.maximum_rates['ore']}, Clay-{self.maximum_rates['clay']}, Obsidian-{self.maximum_rates['obsidian']}"
        )

    def collect(self, resources: dict, robots: dict):
        """Spend time collecting resources"""
        for resource in resources:
            resources[resource] += robots[resource]


    def build_robot(self, resources: dict, robots: dict, robot_type: str):
        """Increase number of robots"""
        if robots[robot_type] >= self.maximum_rates[robot_type]:
            return False  # Don't bother going over maximum useful
        for resource in self.costs[robot_type]:
            resources[resource] -= self.costs[robot_type][resource]
        robots[robot_type] += 1
        for resource in resources.values():
            if resource < 0:
                return False
        return True


    def is_worth_saving(self, resources: dict, robots: dict) -> bool:
        """Returns True if it could be worth saving up this round"""
        if robots["ore"] >= self.maximum_rates["ore"]:
            return False
        if resources["ore"] < self.maximum_rates["ore"]:
            return True
        return False

    def take_turn(
        self,
        resources: dict,
        robots: dict,
        time_left: int,
        to_do: str,
    ):
        """Execute a single 1 minute round of the game"""
        if time_left == 1:
            return resources["geode"] + robots["geode"]

        match to_do:
            case "ore" | "clay" | "obsidian" | "geode":
                if not self.build_robot(resources, robots, to_do):
                    return -1
                self.collect(resources, robots)
                resources[to_do] -= 1  # Take account of robot that was just built
            case _:
                self.collect(resources, robots)
        results = []
        for next_step in ["geode", "obsidian", "clay", "ore"]:
            results.append(
                self.take_turn(
                    resources.copy(), robots.copy(), time_left - 1, next_step
                )
            )
        if max(results) == -1:  # i.e. nothing could be built
            results.append(
                self.take_turn(resources.copy(), robots.copy(), time_left - 1, "save")
            )
        elif self.is_worth_saving(resources, robots):
            results.append(
                self.take_turn(resources.copy(), robots.copy(), time_left - 1, "save")
            )
        return max(results)

    def run_game(self) -> int:
        """Return Maximum number of geodes that can be harvested in a game"""
        initial_resources = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
        initial_robots = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}
        initial_time = self.game_time
        return self.take_turn(initial_resources, initial_robots, initial_time, "save")

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
    blueprints = parse_input(PUZZLE_INPUT)
    total = 0
    for index, blueprint in blueprints.items():
        start = perf_counter()
        total += Game(index, blueprint, 24).get_quality_score()
        end = perf_counter()
        print(f"Blueprint {index} assessed in {end-start}")
    print(total)

    for index, blueprint in blueprints.items():
        if index == 4:
            break
        start = perf_counter()
        total *= Game(index, blueprint, 32).run_game()
        end = perf_counter()
        print(f"Blueprint {index} assessed in {end-start}")
    print(total)


if __name__ == "__main__":
    main()
