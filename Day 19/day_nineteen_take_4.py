from time import perf_counter

from day_nineteen_input import EXAMPLE_INPUT, PUZZLE_INPUT


class DoubleTree:
    def __init__(self, index: int, blueprint: dict, game_time: int = 24) -> None:
        self.game_time = game_time
        self.index = index
        self.costs = blueprint
        self.maxima = {
            "ore": max(self.costs[x]["ore"] for x in self.costs),
            "clay": self.costs["obsidian"]["clay"],
            "obsidian": self.costs["geode"]["obsidian"],
        }
        self.paths = {0: {0: {0: {0: {0: {1: {0: 0}}}}}}}
        print(f"Game {self.index} created:")

        print(f"Blueprint: {self.costs}")
        print(
            f"Maximums: Ore-{self.maxima['ore']}, Clay-{self.maxima['clay']}, Obsidian-{self.maxima['obsidian']}"
        )

    def build_option_combos(self, starting_combo):
        """Return list of possible combos"""
        options = []
        g, g_r, ob, ob_r, o, o_r, c, c_r = starting_combo
        # Build Geode Robot
        if o >= self.costs["geode"]["ore"] and ob >= self.costs["geode"]["obsidian"]:
            options.append(
                [
                    g + g_r,
                    g_r + 1,
                    ob + ob_r - self.costs["geode"]["obsidian"],
                    ob_r,
                    o + o_r - self.costs["geode"]["ore"],
                    o_r,
                    c + c_r,
                    c_r,
                ]
            )
        # Build Obsidian Robot
        if (
            o >= self.costs["obsidian"]["ore"]
            and c >= self.costs["obsidian"]["clay"]
            and ob_r < self.maxima["obsidian"]
        ):
            options.append(
                [
                    g + g_r,
                    g_r,
                    ob + ob_r,
                    ob_r + 1,
                    o + o_r - self.costs["obsidian"]["ore"],
                    o_r,
                    c + c_r - self.costs["obsidian"]["clay"],
                    c_r,
                ]
            )
        # Build Clay Robot
        if o >= self.costs["clay"]["ore"] and c_r < self.maxima["clay"]:
            options.append(
                [
                    g + g_r,
                    g_r,
                    ob + ob_r,
                    ob_r,
                    o + o_r - self.costs["clay"]["ore"],
                    o_r,
                    c + c_r,
                    c_r + 1,
                ]
            )
        # Build Ore Robot
        if o >= self.costs["ore"]["ore"] and o_r < self.maxima["ore"]:
            options.append(
                [
                    g + g_r,
                    g_r,
                    ob + ob_r,
                    ob_r,
                    o + o_r - self.costs["ore"]["ore"],
                    o_r + 1,
                    c + c_r,
                    c_r,
                ]
            )
        # Save
        options.append(
            [
                g + g_r,
                g_r,
                ob + ob_r,
                ob_r,
                o + o_r,
                o_r,
                c + c_r,
                c_r,
            ]
        )
        return options

    def add_combo_to_tree(self, combo, tree):
        a, b, c, d, e, f, g, h = combo
        try:
            tree[a][b][c][d][e][f][g] = max(h, tree[a][b][c][d][e][f][g])
        except KeyError:
            if tree.get(a) is None:
                tree[a] = {b: {c: {d: {e: {f: {g: h}}}}}}
            elif tree[a].get(b) is None:
                tree[a][b] = {c: {d: {e: {f: {g: h}}}}}
            elif tree[a][b].get(c) is None:
                tree[a][b][c] = {d: {e: {f: {g: h}}}}
            elif tree[a][b][c].get(d) is None:
                tree[a][b][c][d] = {e: {f: {g: h}}}
            elif tree[a][b][c][d].get(e) is None:
                tree[a][b][c][d][e] = {f: {g: h}}
            elif tree[a][b][c][d][e].get(f) is None:
                tree[a][b][c][d][e][f] = {g: h}
            elif tree[a][b][c][d][e][f].get(g) is None:
                tree[a][b][c][d][e][f][g] = h

    def play_round(self):
        new_paths = {}
        for g, a in self.paths.items():
            for g_r, b in a.items():
                for ob, c in b.items():
                    for ob_r, d in c.items():
                        for o, e in d.items():
                            for o_r, f in e.items():
                                for c, c_r in f.items():
                                    combo = [g, g_r, ob, ob_r, o, o_r, c, c_r]
                                    for option in self.build_option_combos(combo):
                                        self.add_combo_to_tree(option, new_paths)

        self.paths = new_paths

    def print_combos(self, summary_only: bool = False) -> None:
        total = 0
        if not summary_only:
            print(
                "============================================================================"
            )
            print(
                "geodes|geode_robots|obsidian|obsidian_robots|ore|ore_robots|clay|clay_robots"
            )
            print(
                "----------------------------------------------------------------------------"
            )
        for g, a in self.paths.items():
            for g_r, b in a.items():
                for ob, c in b.items():
                    for ob_r, d in c.items():
                        for o, e in d.items():
                            for o_r, f in e.items():
                                for c, c_r in f.items():
                                    if not summary_only:
                                        print(
                                            f"{g}     | {g_r}          | {ob}      | {ob_r}             | {o} | {o_r}        | {c}  | {c_r}"
                                        )
                                    total += 1
        if not summary_only:
            print(
                "============================================================================"
            )
        print(f"{total} combos")

    def get_combos(self) -> None:
        total = 0
        for g, a in self.paths.items():
            for g_r, b in a.items():
                for ob, c in b.items():
                    for ob_r, d in c.items():
                        for o, e in d.items():
                            for o_r, f in e.items():
                                for c, c_r in f.items():
                                    total += 1
        return total

    def run_game(self) -> int:
        """Return Maximum number of geodes that can be harvested in a game"""
        for i in range(self.game_time - 1):
            start = perf_counter()
            self.play_round()
            end = perf_counter()
            combos = self.get_combos()
            print(
                f"Round {i+1} Complete in {end-start} seconds with {combos} combos",
                end="\r",
            )
            pass

        return self.get_max_geodes()

    def get_max_geodes(self):
        best = 0
        for geodes, robots in self.paths.items():
            best = max(best, geodes + max(robots.keys()))
        return best

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
    total = 1

    for index, blueprint in blueprints.items():
        if index == 4:
            break
        start = perf_counter()
        geodes = DoubleTree(index, blueprint, 32).run_game()
        end = perf_counter()
        total *= geodes
        print(f"Blueprint {index} assessed in {end-start} Total Geodes={geodes}")
    print(total)

    for index, blueprint in blueprints.items():
        start = perf_counter()
        total += DoubleTree(index, blueprint, 24).get_quality_score()
        end = perf_counter()
        print(f"Blueprint {index} assessed in {end-start}")
    print(total)


if __name__ == "__main__":
    main()
