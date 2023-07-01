from math import ceil

rocks = [
    {(0, 0), (1, 0), (2, 0), (3, 0)},
    {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)},
    {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)},
    {(0, 0), (0, 1), (0, 2), (0, 3)},
    {(0, 0), (1, 0), (0, 1), (1, 1)},
]


def simulation(pattern: str):
    next_available = 0
    terrain = set()
    wind_index = 0
    rock_index = 0

    def try_move(rock, dx, dy):
        new_rock = set()
        for x, y in rock:
            nx = x + dx
            ny = y + dy
            if (nx, ny) in terrain:
                return None
            if not 0 <= nx < 7 or not ny >= 0:
                return None
            new_rock.add((nx, ny))
        return new_rock

    while True:
        rock = rocks[rock_index % len(rocks)]
        rock = {(x + 2, next_available + 3 + y) for x, y in rock}

        while True:
            wind = pattern[wind_index]
            if new_rock := try_move(rock, 1 if wind == ">" else -1, 0):
                rock = new_rock
            wind_index = (wind_index + 1) % len(pattern)
            new_rock = try_move(rock, 0, -1)
            if new_rock:
                rock = new_rock
            else:
                break
        terrain.update(rock)
        next_available = max(next_available, max(y for x, y in rock) + 1)
        yield rock_index, wind_index, next_available
        rock_index += 1


def part1(pattern: str):
    for rock_index, _, height in simulation(pattern):
        if rock_index + 1 == 2022:
            return height


def part2(pattern: str):
    completion = {}
    result = []
    for rock_index, wind_index, height in simulation(pattern):
        result.append(height)
        if rock_index % len(rocks) != 0:
            continue
        if wind_index not in completion:
            completion[wind_index] = []
        completion[wind_index].append(rock_index)
        if rock_index == 10000:
            break
    # print(completion)
    completion = {
        k: list(b - a for a, b in zip(v[-4:], v[-3:]))
        for k, v in completion.items()
        if len(v) > 4
    }
    detected_wind_indices = {k for k, v in completion.items() if len(set(v)) == 1}
    # print(detected_wind_indices)
    cycle = max(v[-1] for k, v in completion.items() if k in detected_wind_indices)
    
    
    # print(completion.keys())
    # for k, v in completion.items():
    #     diff = (b - a for a, b in zip(v, v[1:]))
    #     print(k, list(diff))
    #     print(len(v), len(set(v)))
    print(detected_wind_indices)
    print(f"{cycle=}, {len(result)=}")
    for i in range(100):
        if (i + 1) * cycle >= len(result):
            break
        current = result[i * cycle]
        next_height = result[(i + 1) * cycle]
        print(i, i * cycle, current, next_height, next_height - current)
        
    max_recorded_height_index = (len(result) - 1) // cycle * cycle
    print(f"{cycle=}, {len(result)=}")
    height_increse = result[max_recorded_height_index] - result[max_recorded_height_index - cycle]
    print(f"{max_recorded_height_index=}, {height_increse=}")
    target_index = 1000000000000 - 1
    num_cycles = ceil((target_index - len(result) + 1) / cycle)
    index = target_index - num_cycles * cycle
    print(f"{num_cycles=}, {index=}")
    return result[index] + num_cycles * height_increse
    


def test():
    pattern = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
    assert part1(pattern) == 3068
    assert part2(pattern) == 1514285714288


if __name__ == "__main__":
    with open("input/17.txt") as f:
        pattern = f.read().strip()
    print(part1(pattern))
    print(part2(pattern))
