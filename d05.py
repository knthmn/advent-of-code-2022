import re


def parse_input(lines: list[str]) -> tuple[list[list[str]], list[tuple[int, ...]]]:
    blank = lines.index("\n")
    stacks, instructions = lines[:blank], lines[blank + 1 :]
    stacks = [line[1::4] for line in stacks]
    stacks = [[c for c in line[:-1] if c != " "][::-1] for line in zip(*stacks)]
    instructions = [
        tuple(
            int(number)
            for number in re.match(
                R"""move (\d+) from (\d) to (\d)""", line.strip()
            ).groups()
        )
        for line in instructions
    ]
    return stacks, instructions


def part1(lines):
    stacks, instructions = parse_input(lines)
    for amount, src, dst in instructions:
        for _ in range(amount):
            stacks[dst - 1].append(stacks[src - 1].pop())
    return "".join(stack[-1] for stack in stacks)


def part2(lines):
    stacks, instructions = parse_input(lines)
    for amount, src, dst in instructions:
        stacks[dst - 1].extend(stacks[src - 1][-amount:])
        del stacks[src - 1][-amount:]
    return "".join(stack[-1] for stack in stacks)


def test():
    with open("d05-t.txt") as f:
        lines = f.readlines()
    assert part1(lines) == "CMZ"
    assert part2(lines) == "MCD"


if __name__ == "__main__":
    with open("input/05.txt") as f:
        lines = f.readlines()
    print(part1(lines), part2(lines))
