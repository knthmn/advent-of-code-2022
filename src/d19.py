import re
from dataclasses import dataclass, replace

pattern = r"""Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."""


@dataclass(frozen=True, slots=True)
class Material:
    ore: int
    clay: int
    obsidian: int
    geode: int

    def copy(self, **changes):
        return replace(self, **changes)

    def __add__(self, other: "Material"):
        return Material(
            self.ore + other.ore,
            self.clay + other.clay,
            self.obsidian + other.obsidian,
            self.geode + other.geode,
        )

    def __sub__(self, other: "Material"):
        return Material(
            self.ore - other.ore,
            self.clay - other.clay,
            self.obsidian - other.obsidian,
            self.geode - other.geode,
        )


def quality_level(line: str, allowed_time: int) -> tuple[int, int]:
    match = re.match(pattern, line)
    assert match is not None
    groups = [int(num) for num in match.groups()]

    ore_bot_cost = Material(groups[1], 0, 0, 0)
    clay_bot_cost = Material(groups[2], 0, 0, 0)
    obsidian_bot_cost = Material(groups[3], groups[4], 0, 0)
    geode_bot_cost = Material(groups[5], 0, groups[6], 0)
    max_ore_cost = max(ore_bot_cost.ore, clay_bot_cost.ore, obsidian_bot_cost.ore, geode_bot_cost.ore)

    global_max_geode = 0

    def search(
        resources: Material,
        bots: Material,
        time: int,
        opportunity: Material = Material(1, 1, 1, 1),
    ) -> int:
        nonlocal global_max_geode

        max_geode = resources.geode
        if time == allowed_time:
            return max_geode

        remaining_time = allowed_time - time
        max_possible_geode = (
            max_geode
            + bots.geode * remaining_time
            + (remaining_time - 1) * remaining_time // 2
        )
        if max_possible_geode <= global_max_geode:
            return global_max_geode

        enough_ore = resources.ore >= ore_bot_cost.ore
        enough_clay = resources.ore >= clay_bot_cost.ore
        enough_obsidian = (
            resources.ore >= obsidian_bot_cost.ore and resources.clay >= obsidian_bot_cost.clay
        )
        enough_geode = (
            resources.ore >= geode_bot_cost.ore
            and resources.obsidian >= geode_bot_cost.obsidian
        )

        if enough_geode and opportunity.geode:
            max_geode = max(
                max_geode,
                search(
                    resources + bots - geode_bot_cost, bots + Material(0, 0, 0, 1), time + 1, 
                ),
            )
        if enough_obsidian and opportunity.obsidian and bots.obsidian < geode_bot_cost.obsidian:
            max_geode = max(
                max_geode,
                search(
                    resources + bots - obsidian_bot_cost,
                    bots + Material(0, 0, 1, 0),
                    time + 1,
                ),
            )
        if enough_clay and opportunity.clay and bots.clay < obsidian_bot_cost.clay:
            max_geode = max(
                max_geode,
                search(
                    resources + bots - clay_bot_cost, bots + Material(0, 1, 0, 0), time + 1
                ),
            )
        if enough_ore and opportunity.ore and bots.ore < max_ore_cost:
            max_geode = max(
                max_geode,
                search(
                    resources + bots - ore_bot_cost, bots + Material(1, 0, 0, 0), time + 1
                ),
            )
        max_geode = max(
            max_geode,
            search(
                resources + bots,
                bots,
                time + 1,
                Material(
                    int(not enough_ore and opportunity.ore),
                    int(not enough_clay and opportunity.clay),
                    int(not enough_obsidian and opportunity.obsidian),
                    int(not enough_geode and opportunity.obsidian),
                ),
            ),
        )

        if max_geode > global_max_geode:
            global_max_geode = max_geode

        return max_geode

    return groups[0], search(Material(0, 0, 0, 0), Material(1, 0, 0, 0), 0)


def part1(lines: list[str]):
    acc = 0
    for line in lines:
        blueprint_id, max_geodes = quality_level(line, 24)
        acc += blueprint_id * max_geodes
    return acc


def part2(lines: list[str]):
    acc = 1
    for line in lines[:3]:
        _, max_geodes = quality_level(line, 32)
        acc *= max_geodes
    return acc


def test():
    with open("d19-t.txt") as f:
        lines = f.readlines()
    assert quality_level(lines[0], 24)[1] == 9
    assert quality_level(lines[1], 24)[1] == 12
    assert quality_level(lines[0], 32)[1] == 56
    assert quality_level(lines[1], 32)[1] == 62


if __name__ == "__main__":
    with open("input/19.txt") as f:
        lines = f.readlines()
    print(part1(lines))
    print(part2(lines))
