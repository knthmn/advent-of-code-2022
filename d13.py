import functools


def parse(line: str):
    line = line.strip()[1:-1]
    root = []
    stack = [root]
    saved_digits = []

    def flush_digits():
        if saved_digits:
            stack[-1].append(int("".join(saved_digits)))
            saved_digits.clear()

    for c in line:
        if c.isdigit():
            saved_digits.append(c)
            continue
        flush_digits()
        if c == "[":
            sublist = []
            stack[-1].append(sublist)
            stack.append(sublist)
        elif c == "]":
            stack.pop()
    flush_digits()
    return root


def compare(first, second) -> bool | None:
    # print("comparing", first, second, type(first, ))
    for a, b in zip(first, second):
        if isinstance(a, int) and isinstance(b, int):
            if a != b:
                return a < b
            else:
                continue
        if not isinstance(a, list):
            a = [a]
        if not isinstance(b, list):
            b = [b]
        comparison = compare(a, b)
        if comparison is not None:
            return comparison
    if len(first) != len(second):
        return len(first) < len(second)
    return None


def part1(lines: list[str]):
    sections = [
        lines[pair_index * 3 : (pair_index + 1) * 3 - 1]
        for pair_index in range((len(lines) + 1) // 3)
    ]
    pairs = [[parse(line) for line in section] for section in sections]

    return sum(index + 1 for index, pair in enumerate(pairs) if compare(*pair))


def part2(lines: list[str]):
    packets = [parse(line) for line in lines if line.strip()]
    dividers = [[[2]], [[6]]]
    packets.extend(dividers)
    packets.sort(key=functools.cmp_to_key(lambda a, b: -1 if compare(a, b) else 1))
    return (packets.index(dividers[0]) + 1) * (packets.index(dividers[1]) + 1)


def test():
    with open("d13-t.txt") as f:
        lines = f.readlines()
    assert part1(lines) == 13
    assert part2(lines) == 140


if __name__ == "__main__":
    with open("input/13.txt") as f:
        lines = f.readlines()
    print(part1(lines))
    print(part2(lines))
