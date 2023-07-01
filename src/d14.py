import itertools
from typing import Callable

Point = tuple[int, int]


def parse_walls(lines: list[str]) -> set[Point]:
    material = set()
    for line in lines:
        line = line.strip()
        points = [
            tuple(int(coord) for coord in point.split(","))
            for point in line.split(" -> ")
        ]
        for (start_x, start_y), (end_x, end_y) in zip(points[:-1], points[1:]):
            min_x, max_x = min(start_x, end_x), max(start_x, end_x)
            min_y, max_y = min(start_y, end_y), max(start_y, end_y)
            for x, y in itertools.product(
                range(min_x, max_x + 1), range(min_y, max_y + 1)
            ):
                material.add((x, y))
    return material


def fall(
    init_pos: Point,
    is_free: Callable[[Point], bool],
    terminate: Callable[[Point], bool],
) -> Point | None:
    x, y = init_pos
    while True:
        for nx in [x, x - 1, x + 1]:
            if is_free((nx, y + 1)):
                y += 1
                x = nx
                break
        else:
            return x, y
        if terminate((x, y)):
            return None


def part1(lines: list[str]):
    material = parse_walls(lines)
    num_settled = 0
    max_y = max(y for _, y in material)
    while True:
        final = fall(
            (500, 0),
            lambda point: point not in material,
            lambda point: point[1] > max_y,
        )
        if final:
            material.add(final)
            num_settled += 1
        else:
            return num_settled


def part2(lines: list[str]):
    material = parse_walls(lines)
    num_settled = 0
    wall_y = max(y for _, y in material) + 2
    while True:
        final = fall(
            (500, 0),
            lambda point: point not in material and point[1] != wall_y,
            lambda _: False,
        )
        material.add(final)
        num_settled += 1
        if (500, 0) in material:
            return num_settled


def test():
    with open("d14-t.txt") as f:
        lines = f.readlines()
    assert part1(lines) == 24
    assert part2(lines) == 93


if __name__ == "__main__":
    with open("input/14.txt") as f:
        lines = f.readlines()
    print(part1(lines))
    print(part2(lines))
