"""Advent of Code 2022 Day 16 Solution"""

from day_sixteen_input import EXAMPLE_INPUT, PUZZLE_INPUT


def process_input(input_description: str) -> tuple:
    """Returns Unweighted graph of connected locations and dictionary of valve flow rates"""
    input_entries = input_description.splitlines()

    cave_layout = {}
    valves = {}

    for input_entry in input_entries:
        # "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
        _, room, _, _, rate, _, _, _, _, *next_rooms = input_entry.split()
        cleansed_next_rooms = []
        for next_room in next_rooms:
            next_room = next_room.strip()
            if next_room[-1] == ",":
                next_room = next_room[:-1]
            cleansed_next_rooms.append(next_room)

        cave_layout[room] = cleansed_next_rooms
        rate = int(rate[5:-1])
        if rate or room == "AA":
            valves[room] = rate

    return cave_layout, valves


def get_shortest_path(graph: dict, start: str, end: str, path: list) -> int:
    """Return shortest distance between two points on an unweighted graph"""
    if start == end:
        return len(path)

    best_from_here = None
    for node in graph[start]:
        if node not in path:
            length = get_shortest_path(graph, node, end, [start] + path)
            if length is not None:
                if best_from_here is None or best_from_here > length:
                    best_from_here = length
    return best_from_here


def simplify_graph(graph_layout: dict, nodes_of_interest: set):
    """Returns a weighted graph containing all nodes_of_interest, where each edge is the distance between nodes"""
    new_graph = {}

    for node_a in nodes_of_interest:
        new_dict = {}
        for node_b in nodes_of_interest:
            if node_a == node_b:
                continue
            new_dict[node_b] = get_shortest_path(graph_layout, node_a, node_b, [])
        new_graph[node_a] = new_dict
    return new_graph


def calculate_total_flow(flow_rates: dict, valves_open: dict) -> int:
    """
    flow_rates is dictionary of Valve: Rate
    valves_open is a dictionary of Valve: Time_left when open
    """
    total = 0
    for valve_name, valve_time in valves_open.items():
        total += valve_time * flow_rates[valve_name]
    return total


def max_flow(
    graph: dict,
    valves_open: dict,
    time_left: int,
    current_node: str,
    best_flow: int,
    flow_rates: dict,
) -> int:
    """
    Return dictionary of open valves when timer runs out
    valves_open is a dictionary of how much time was left when a valve was opened
    """
    if time_left <= 1:
        return calculate_total_flow(flow_rates, valves_open)
    if len(valves_open.keys()) == len(graph.keys()) - 1:
        return calculate_total_flow(flow_rates, valves_open)

    new_valves_open = valves_open.copy()
    if flow_rates[current_node]:
        time_left -= 1
        new_valves_open[current_node] = time_left

    for next_node in graph[current_node]:
        if next_node in valves_open:
            continue
        new_time = time_left - graph[current_node][next_node]
        flow = max_flow(
            graph, new_valves_open, new_time, next_node, best_flow, flow_rates
        )
        best_flow = max(flow, best_flow)
    return best_flow


def max_flow_achievable(graph: dict, valves: dict, time_left: int):
    """Returns maximum flow_rate achievable in given time"""
    return max_flow(graph, {}, time_left, "AA", 0, valves)


def main():  # pylint:disable=missing-function-docstring

    cave_layout, valve_flow_rates = process_input(PUZZLE_INPUT)

    simplified_graph = simplify_graph(cave_layout, set(valve_flow_rates.keys()))

    time_until_expiry = 30
    maximum_flow_rate = max_flow_achievable(
        simplified_graph, valve_flow_rates, time_until_expiry
    )
    print(f"Maximum possible flow rate is {maximum_flow_rate}")


if __name__ == "__main__":
    main()
