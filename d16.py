import functools
import re
from collections import deque
from typing import NamedTuple


class Valve(NamedTuple):
    name: str
    flow_rate: int
    tunnels: list[str]


def parse(lines: list[str]) -> dict[str, Valve]:
    valves = {}
    for line in lines:
        name, flow_rate, tunnels = re.match(
            "Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z ,]+)",
            line.strip(),
        ).groups()
        tunnels = [dest.strip() for dest in tunnels.split(",")]
        valves[name] = Valve(name, int(flow_rate), tunnels)
    return valves


def calculate_distance_map(origin, valves):
    distance_map = {origin: 0}
    paths = deque([(origin, 0)])

    while paths and len(distance_map) != len(valves):
        current_name, distance = paths.popleft()
        valve = valves[current_name]
        for dest in valve.tunnels:
            if dest in distance_map:
                continue
            distance_map[dest] = distance + 1
            paths.append((dest, distance + 1))
    return distance_map


def find_maximum_pressure(lines: list[str], initial_time_remaining=30, num_agents=1):
    valves = parse(lines)
    good_valves = set(name for name, pipe in valves.items() if pipe.flow_rate != 0)
    distances = {
        origin: calculate_distance_map(origin, valves)
        for origin in {"AA"} | good_valves
    }

    @functools.cache
    def recursive(agents: tuple[tuple[str, int], ...], turned: frozenset[str]) -> int:
        max_value = 0
        next_valves = good_valves - turned
        for agent_index in range(len(agents)):
            current, time_remaining = agents[agent_index]
            _, flow_rate, tunnels = valves[current]
            new_agents = list(agents)
            for dest in next_valves:
                if distances[current][dest] + 1 >= time_remaining:
                    continue
                new_remaining_time = time_remaining - distances[current][dest] - 1
                new_agents[agent_index] = (dest, new_remaining_time)
                dest_gain = valves[dest].flow_rate * new_remaining_time
                further_gain = recursive(
                    tuple(sorted(new_agents)), frozenset(turned | {dest})
                )
                max_value = max(max_value, dest_gain + further_gain)
        return max_value

    return recursive((("AA", initial_time_remaining),) * num_agents, frozenset())


def test():
    with open("d16-t.txt") as f:
        lines = f.readlines()
    assert find_maximum_pressure(lines) == 1651
    assert find_maximum_pressure(lines, 26, 2) == 1707


if __name__ == "__main__":
    with open("input/16.txt") as f:
        lines = f.readlines()
    print(find_maximum_pressure(lines))
    print(find_maximum_pressure(lines, 26, 2))
