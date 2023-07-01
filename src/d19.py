import re

pattern = r"""Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."""


def quality_level(line: str, time: int):
    groups = [int(num) for num in re.match(pattern, line).groups()]
    blueprint_id = groups[0]
    ore_cost = groups[1], 0, 0
    clay_cost = groups[2], 0, 0
    obsidian_cost = groups[3], groups[4], 0
    geode_cost = groups[5], 0, groups[6]

    states = {(0, 0, 0, 0, 1, 0, 0)}
    t = 0
    while True:
        new_states = set()
        for state in states:
            resources = state[:3]
            geode = state[3]
            bots = state[4:]
            ore_bot, clay_bot, obsidian_bot = bots
            next_resources = tuple(a + b for a, b in zip(resources, bots))
            possibility = 0
            if all(a >= b for a, b in zip(resources, ore_cost)) and ore_bot:
                possibility += 1
                consumed = tuple(a - b for a, b in zip(next_resources, ore_cost))
                new_states.add((*consumed, geode, ore_bot + 1, clay_bot, obsidian_bot))
            if all(a >= b for a, b in zip(resources, clay_cost)):
                possibility += 1
                consumed = tuple(a - b for a, b in zip(next_resources, clay_cost))
                new_states.add((*consumed, geode, ore_bot, clay_bot + 1, obsidian_bot))
            if all(a >= b for a, b in zip(resources, obsidian_cost)):
                possibility += 1
                consumed = tuple(a - b for a, b in zip(next_resources, obsidian_cost))
                new_states.add((*consumed, geode, ore_bot, clay_bot, obsidian_bot + 1))
            if all(a >= b for a, b in zip(resources, geode_cost)):
                possibility += 1
                consumed = tuple(a - b for a, b in zip(next_resources, geode_cost))
                new_states.add((*consumed, geode + (time - t - 1), *bots))
            if possibility != 4:
                new_states.add((*next_resources, geode, *bots))
        states = new_states

        t += 1
        if t == time:
            break

        filtered_states = set()
        # I don't know what +10 works, I tried +1 and +2. Maybe I am reasoning
        # this wrong so a buffer is needed, investigate further.
        for state in states:
            ore, clay, obsidian, geode, ore_bot, clay_bot, obsidian_bot = state
            max_cost_ore = max(
                cost[0] for cost in (ore_cost, clay_cost, obsidian_cost, geode_cost)
            )
            if ore >= (max_cost_ore - ore_bot) * (time - t - 1) and ore >= max_cost_ore:
                ore = min(ore, max_cost_ore + 10)
                ore_bot = min(ore_bot, max_cost_ore + 10)
            if (
                clay >= (obsidian_cost[1] - clay_bot) * (time - t - 1)
                and clay >= obsidian_cost[1]
            ):
                clay = min(clay, obsidian_cost[1] + 10)
                clay_bot = min(clay_bot, obsidian_cost[1] + 10)
            if (
                obsidian >= (geode_cost[2] - obsidian_bot) * (time - t - 1)
                and obsidian >= geode_cost[2]
            ):
                obsidian = min(obsidian, geode_cost[2] + 10)
                obsidian_bot = min(obsidian_bot, geode_cost[2] + 10)
            filtered_states.add(
                (ore, clay, obsidian, geode, ore_bot, clay_bot, obsidian_bot)
            )
        states = filtered_states

        # this part runs at n^2, but in the end it removes enough states that
        # the runtime is pretty much the same
        filtered_states = set(states)
        for ref_state in states:
            if ref_state not in filtered_states:
                continue
            new_filtered_states = set()
            for state in filtered_states:
                if state == ref_state:
                    new_filtered_states.add(state)
                elif not all(a <= b for a, b in zip(state, ref_state)):
                    new_filtered_states.add(state)
            filtered_states = new_filtered_states
        states = filtered_states

    return blueprint_id, max(state[3] for state in states)


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
