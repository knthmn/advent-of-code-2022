rocks = [
    {(0, 0), (1, 0), (2, 0), (3, 0)},
    {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)},
    {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)},
    {(0, 0), (0, 1), (0, 2), (0, 3)},
    {(0, 0), (1, 0), (0, 1), (1, 1)},
]


def part1(pattern: str):
    highest = -1
    terrain = set()
    wind_index = 0

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

    for rock_index in range(2022):
        rock = rocks[rock_index % len(rocks)]
        rock = {(x + 2, highest + 3 + y + 1) for x, y in rock}

        while True:
            wind = pattern[wind_index % len(pattern)]
            if new_rock := try_move(rock, 1 if wind == ">" else -1, 0):
                rock = new_rock
            wind_index += 1
            new_rock = try_move(rock, 0, -1)
            if new_rock:
                rock = new_rock
            else:
                break
        terrain.update(rock)
        highest = max(highest, max(y for x, y in rock))

    return highest + 1


def part2(pattern: str):
    ...


def test():
    pattern = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
    assert part1(pattern) == 3068
    # assert part2(lines) == None


if __name__ == "__main__":
    with open("input/17.txt") as f:
        pattern = f.read().strip()
    print(part1(pattern))
    print(part2(pattern))
