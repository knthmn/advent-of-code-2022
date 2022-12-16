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


def part1(lines: list[str]):
    valves = parse(lines)
    good_valves = set(name for name, pipe in valves.items() if pipe.flow_rate != 0)

    def generate_distances(origin):
        distances = {origin: 0}
        paths = deque([(origin, 0)])

        while paths and len(distances) != len(valves):
            current_name, distance = paths.popleft()
            valve = valves[current_name]
            for dest in valve.tunnels:
                if dest in distances:
                    continue
                distances[dest] = distance + 1
                paths.append((dest, distance + 1))
        return {
            dest: distance
            for dest, distance in distances.items()
            if dest in good_valves and dest != origin
        }

    distances = {origin: generate_distances(origin) for origin in {"AA"} | good_valves}

    def find_max_pressure(
        current: str, remaining_time: int, acc: int, turned: set[str]
    ) -> int:
        if remaining_time <= 0 or len(turned) == len(good_valves):
            return acc
        _, flow_rate, tunnels = valves[current]
        next_valves = good_valves - turned - {current}
        max_pressure = max(
            find_max_pressure(
                dest,
                remaining_time - distances[current][dest] - 1,
                acc
                + max(0, remaining_time - distances[current][dest] - 1)
                * valves[dest].flow_rate,
                turned | {dest},
            )
            for dest in next_valves
        )
        return max_pressure

    return find_max_pressure("AA", 30, 0, set())


def part2(lines: list[str]):
    ...


def test():
    with open("d16-t.txt") as f:
        lines = f.readlines()
    assert part1(lines) == 1651
    assert part2(lines) == None


if __name__ == "__main__":
    with open("input/16.txt") as f:
        lines = f.readlines()
    print(part1(lines))
    print(part2(lines))
