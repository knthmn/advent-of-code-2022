from functools import reduce


def priority(item: str) -> int:
    return ord(item) - ord("a") + 1 if item.islower() else ord(item) - ord("A") + 27


def part1(lines: list[str]) -> int:
    acc = 0
    for line in lines:
        line = line.strip()
        mid = len(line) // 2
        first, second = set(line[:mid]), set(line[mid:])
        common = (first & second).pop()
        acc += priority(common)
    return acc


def part2(lines: list[str]) -> int:
    acc = 0
    for index_group in range(len(lines) // 3):
        group = (
            set(elf.strip()) for elf in lines[index_group * 3 : (index_group + 1) * 3]
        )
        common = reduce(lambda x, y: x & y, group).pop()
        acc += priority(common)
    return acc


def test():
    with open("d03-t.txt") as f:
        lines = f.readlines()
    assert part1(lines) == 157
    assert part2(lines) == 70


if __name__ == "__main__":
    with open("input/03.txt") as f:
        lines = f.readlines()
    print(part1(lines), part2(lines))
