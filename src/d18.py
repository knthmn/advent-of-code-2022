def neighbors(x, y, z):
    yield x + 1, y, z
    yield x - 1, y, z
    yield x, y + 1, z
    yield x, y - 1, z
    yield x, y, z + 1
    yield x, y, z - 1


def part1(lines: list[str]):
    lava = {tuple(int(coord) for coord in line.split(",")) for line in lines}
    acc = 0
    for x, y, z in lava:
        acc += 6
        for nx, ny, nz in neighbors(x, y, z):
            if (nx, ny, nz) in lava:
                acc -= 1
    return acc


def part2(lines: list[str]):
    lava = {tuple(int(coord) for coord in line.split(",")) for line in lines}
    min_coord = tuple(min(coord[i] for coord in lava) for i in range(3))
    max_coord = tuple(max(coord[i] for coord in lava) for i in range(3))

    visited = set()
    surface_air = set()
    search = [tuple(x - 1 for x in min_coord)]
    while search:
        x, y, z = search.pop()
        if any((neighbor in lava) for neighbor in neighbors(x, y, z)):
            surface_air.add((x, y, z))
        for neighbor in neighbors(x, y, z):
            if neighbor in visited or not all(
                mi - 1 <= c <= ma + 1
                for mi, c, ma in zip(min_coord, neighbor, max_coord)
            ) or neighbor in lava:
                continue
            visited.add(neighbor)
            search.append(neighbor)

    acc = 0
    for x, y, z in surface_air:
        for nx, ny, nz in neighbors(x, y, z):
            if (nx, ny, nz) in lava:
                acc += 1
    return acc


def test():
    with open("d18-t.txt") as f:
        lines = f.readlines()
    assert part1(lines) == 64
    assert part2(lines) == 58


if __name__ == "__main__":
    with open("input/18.txt") as f:
        lines = f.readlines()
    print(part1(lines))
    print(part2(lines))
