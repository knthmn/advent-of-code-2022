from collections import Counter

directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]


def parse(lines: list[str]):
    return {
        (x, y)
        for y, line in enumerate(lines)
        for x, c in enumerate(line.strip())
        if c == "#"
    }


def step(elves, first_direction):
    proposals = {}
    for elf in elves:
        x, y = elf
        neighbors = ((x + dx, y + dy) for dx in range(-1, 2) for dy in range(-1, 2))
        if all(neighbor not in elves or neighbor == elf for neighbor in neighbors):
            proposals[elf] = elf
            continue
        for direction_shift in range(4):
            dx, dy = directions[(first_direction + direction_shift) % 4]
            check_locations = (
                ((x + cx, y + dy) for cx in range(-1, 2))
                if dx == 0
                else ((x + dx, y + cy) for cy in range(-1, 2))
            )
            if all(check_location not in elves for check_location in check_locations):
                proposals[elf] = x + dx, y + dy
                break
            else:
                proposals[elf] = elf
    counter = Counter(proposals.values())
    new_elves = set()
    for elf in elves:
        if counter[proposals[elf]] == 1:
            new_elves.add(proposals[elf])
        else:
            new_elves.add(elf)
    return new_elves


def part1(lines: list[str]):
    elves = parse(lines)
    for t in range(10):
        elves = step(elves, t % len(directions))
    len_x = max(x for x, _ in elves) - min(x for x, _ in elves) + 1
    len_y = max(y for _, y in elves) - min(y for _, y in elves) + 1

    return len_y * len_x - len(elves)


def part2(lines: list[str]):
    elves = parse(lines)
    t = 0
    while True:
        new_elves = step(elves, t % len(directions))
        t += 1
        if elves == new_elves:
            return t
        elves = new_elves


def test():
    with open("d23-t.txt") as f:
        lines = f.readlines()
    assert part1(lines) == 110
    assert part2(lines) == 20


if __name__ == "__main__":
    with open("input/23.txt") as f:
        lines = f.readlines()
    print(part1(lines))
    print(part2(lines))
