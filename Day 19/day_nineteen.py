from time import perf_counter
from day_nineteen_input import EXAMPLE_INPUT, PUZZLE_INPUT


class Game:
    def __init__(self, index: int, blueprint: dict, game_time: int = 24) -> None:
        self.game_time = game_time
        self.index = index
        self.costs = blueprint
        self.maximum_ore = max(self.costs[x]["ore"] for x in self.costs)
        self.maximum_clay = self.costs["obsidian"]["clay"]
        self.maximum_obsidian = self.costs["geode"]["obsidian"]
        self.maximum_rates = {
            "ore": self.maximum_ore,
            "clay": self.maximum_clay,
            "obsidian": self.maximum_obsidian,
            "geode": 1000,
        }
        print(f"Game {self.index} created:")
        print(f"Blueprint: {self.costs}")
        print(
            f"Maximums: Ore-{self.maximum_ore}, Clay-{self.maximum_clay}, Obsidian-{self.maximum_obsidian}"
        )

    def save_up(self, resources: dict, robots: dict):
        return resources, robots

    def collect(self, resources: dict, robots: dict):
        """Spend time collecting resources"""
        for resource in resources:
            resources[resource] += robots[resource]

    def build_ore_robot(self, resources: dict, robots: dict):
        return self.build_robot(resources, robots, "ore")

    def build_clay_robot(self, resources: dict, robots: dict):
        return self.build_robot(resources, robots, "clay")

    def build_obsidian_robot(self, resources: dict, robots: dict):
        return self.build_robot(resources, robots, "obsidian")

    def build_geode_robot(self, resources: dict, robots: dict):
        return self.build_robot(resources, robots, "geode")

    def build_robot(self, resources: dict, robots: dict, robot_type: str):
        """Increase number of robots"""
        for resource in self.costs[robot_type]:
            resources[resource] -= self.costs[robot_type][resource]
        robots[robot_type] += 1
        return resources, robots

    def unrestricted_robots_of_type(self, robots: dict, robot_type: str) -> bool:
        """Returns True if I can now make an unrestricted amount of robots of robot_type"""
        for resource in self.costs[robot_type]:
            if robots[resource] < self.costs[robot_type][resource]:
                return False
        return True

    def is_robot_affordable(self, resources: dict, robot_type: str) -> bool:
        """Returns true if given robot type is affordable"""
        for resource in self.costs[robot_type]:
            if resources[resource] < self.costs[robot_type][resource]:
                return False
        return True

    def is_robot_affordable_ore(
        self, resources: dict, robots: dict, robot_type: str
    ) -> bool:
        """Returns true if given robot type is affordable given the amount of ore"""
        if (
            resources["ore"] < self.costs[robot_type]["ore"]
            and robots["ore"] < self.costs[robot_type]["ore"]
        ):
            return False
        return True

    def robot_at_max_rate(self, robots: dict, robot_type: str) -> bool:
        """Returns true if there is no point creating more robots of the given type"""
        return robots[robot_type] >= self.maximum_rates[robot_type]

    def get_options_optimal(self, resources: dict, robots: dict) -> set:
        """Return optimal set of options given resources and robots available"""
        if self.unrestricted_robots_of_type(robots, "geode"):
            if self.is_robot_affordable(resources, "geode"):
                return {self.build_geode_robot}
            return {self.save_up}

        potentials = {"geode", "obsidian", "clay", "ore"}
        for resource in potentials.copy():
            if self.robot_at_max_rate(robots, resource):
                potentials.discard(resource)

        options = []
        for resource in potentials.copy():
            if not self.is_robot_affordable_ore(resources, robots, resource):
                options.append(self.save_up)
            if not self.is_robot_affordable(resources, resource):
                potentials.discard(resource)

        if "ore" in potentials:
            options.insert(0, self.build_ore_robot)
        if "clay" in potentials:
            options.insert(0, self.build_clay_robot)
        if "obsidian" in potentials:
            options.insert(0, self.build_obsidian_robot)
        if "geode" in potentials:
            options.insert(0, self.build_geode_robot)

        return options

    def get_options(self, resources: dict, robots: dict) -> set:
        """Return set of options given resources available"""
        options = set()
        if (
            resources["ore"] >= self.costs["geode"]["ore"]
            and resources["obsidian"] >= self.costs["geode"]["obsidian"]
        ):
            options.add(self.build_geode_robot)
        if (
            robots["obsidian"] < self.maximum_obsidian
            and resources["ore"] >= self.costs["obsidian"]["ore"]
            and resources["clay"] >= self.costs["obsidian"]["clay"]
        ):
            options.add(self.build_obsidian_robot)
            if (
                resources["ore"] - self.costs["obsidian"]["ore"] + robots["ore"]
                < self.costs["geode"]["ore"]
            ):
                options.add(self.save_up)
        if (
            robots["clay"] < self.maximum_clay
            and resources["ore"] >= self.costs["clay"]["ore"]
        ):
            options.add(self.build_clay_robot)
            if (
                resources["ore"] - self.costs["clay"]["ore"] + robots["ore"]
                < self.costs["geode"]["ore"]
                or resources["ore"] - self.costs["clay"]["ore"] + robots["ore"]
                < self.costs["obsidian"]["ore"]
            ):
                options.add(self.save_up)
        if (
            robots["ore"] < self.maximum_ore
            and resources["ore"] >= self.costs["ore"]["ore"]
        ):
            options.add(self.build_ore_robot)

        if not options:
            options.add(self.save_up)

        return options

    def best_case(self, time_left: int, robots: dict) -> int:
        current_robots = robots["geode"] * time_left
        new_robots = (time_left * (time_left - 1)) // 2
        return current_robots + new_robots

    def take_turn(
        self, resources: dict, robots: dict, time_left: int, best_so_far: int
    ):
        """Execute a single 1 minute round of the game"""
        if time_left == 1:
            return resources["geode"] + robots["geode"]
        if best_so_far >= resources["geode"] + self.best_case(time_left, robots):
            return -1  # no-hoper
        options = self.get_options_optimal(resources, robots)
        self.collect(resources, robots)
        for option in options:
            new_resources, new_robots = option(resources.copy(), robots.copy())
            best_so_far = max(
                best_so_far,
                self.take_turn(new_resources, new_robots, time_left - 1, best_so_far),
            )
        return best_so_far

    def run_game(self) -> int:
        """Return Maximum number of geodes that can be harvested in a game"""
        initial_resources = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
        initial_robots = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}
        initial_time = self.game_time
        return self.take_turn(initial_resources, initial_robots, initial_time, 0)

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
        #total += Game(index, blueprint, 24).get_quality_score()
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
