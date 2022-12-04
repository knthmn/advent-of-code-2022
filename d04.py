import re
from typing import Callable


def count(lines: list[str], condition: Callable[[int, int, int, int], bool]):
    acc = 0
    for line in lines:
        ints = [
            int(digit)
            for digit in re.match(R"""(\d+)-(\d+),(\d+)-(\d+)""", line.strip()).groups()
        ]
        if condition(*ints):
            acc += 1
    return acc


def part1(lines: list[str]):
    return count(
        lines, lambda a1, a2, b1, b2: a1 <= b1 <= b2 <= a2 or b1 <= a1 <= a2 <= b2
    )


def part2(lines: list[str]):
    return count(
        lines,
        lambda a1, a2, b1, b2: b1 <= a1 <= b2
        or b1 <= a2 <= b2
        or a1 <= b1 <= a2
        or a1 <= b2 <= a2,
    )


def test():
    with open("d04-t.txt") as f:
        lines = f.readlines()
    assert part1(lines) == 2
    assert part2(lines) == 4


if __name__ == "__main__":
    with open("input/04.txt") as f:
        lines = f.readlines()
    print(part1(lines), part2(lines))
