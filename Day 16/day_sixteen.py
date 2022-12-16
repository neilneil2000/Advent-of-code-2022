"""Advent of Code 2022 Day 16 Solution"""

from day_sixteen_input import EXAMPLE_INPUT, PUZZLE_INPUT


def process_input(input_description: str) -> tuple:
    """Returns Unweighted graph of connected locations and dictionary of valve flow rates"""
    return {}, {}


def simplify_graph(graph_layout, nodes_of_interest):
    """Returns a weighted graph containing all nodes_of_interest, where each edge is the distance between nodes"""
    return {}


def max_flow_achievable(graph: dict, valves: dict, time_left: int):
    """Returns maximum flow_rate achievable in given time"""
    return 0


def main():  # pylint:disable=missing-function-docstring

    cave_layout, valve_flow_rates = process_input(EXAMPLE_INPUT)

    simplified_graph = simplify_graph(cave_layout, valve_flow_rates.keys())

    time_until_expiry = 30
    maximum_flow_rate = max_flow_achievable(
        simplified_graph, valve_flow_rates, time_until_expiry
    )
    print(f"Maximum possible flow rate is {maximum_flow_rate}")


if __name__ == "__main__":
    main()
