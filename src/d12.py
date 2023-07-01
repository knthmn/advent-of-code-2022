import collections
from typing import Callable


def search(lines: list[str], start: str, end: str, valid: Callable[[int], bool]):
    def height(x, y):
        c = lines[y][x]
        return 0 if c == "S" else 27 if c == "E" else ord(c) - ord("a") + 1

    start_pos = None
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == start:
                start_pos = (x, y)
    if start_pos is None:
        raise ValueError()

    len_y = len(lines)
    len_x = len(lines[0].strip())
    search = collections.deque([(start_pos, 0)])
    visited = set()

    while search:
        (x, y), steps = search.popleft()
        for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if not 0 <= nx < len_x or not 0 <= ny < len_y:
                continue
            if (nx, ny) in visited:
                continue
            if not valid(height(nx, ny) - height(x, y)):
                continue
            if lines[ny][nx] == end:
                return steps + 1
            search.append(((nx, ny), steps + 1))
            visited.add((nx, ny))
    return None


def part1(lines: list[str]):
    return search(lines, "S", "E", lambda diff: diff <= 1)


def part2(lines: list[str]):
    return search(lines, "E", "a", lambda diff: diff >= -1)


def test():
    with open("d12-t.txt") as f:
        lines = f.readlines()
    assert part1(lines) == 31
    assert part2(lines) == 29


if __name__ == "__main__":
    with open("input/12.txt") as f:
        lines = f.readlines()
    print(part1(lines))
    print(part2(lines))
