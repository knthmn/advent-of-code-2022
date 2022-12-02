import numpy as np


def get_values(content: list[str]):
    values = np.transpose(
        np.loadtxt(content, delimiter=" ", dtype=str, encoding="utf8").view(np.int32)
    )
    return values[0] - ord("A"), values[1] - ord("X")


def part1(content):
    opponent, response = get_values(content)
    win = (response - opponent + 1) % 3
    answer = response + 1 + win * 3
    return np.sum(answer)


def part2(content):
    opponent, win = get_values(content)
    play = (opponent + win - 1) % 3
    answer = play + 1 + win * 3
    return np.sum(answer)


def test():
    with open("d02-t.txt") as f:
        lines = f.readlines()
    assert part1(lines) == 15
    assert part2(lines) == 12


if __name__ == "__main__":
    with open("input/02.txt") as f:
        lines = f.readlines()
    print(part1(lines))
    print(part2(lines))
