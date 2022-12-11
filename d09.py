import numpy as np

directions = {
    "U": np.array([0, -1]),
    "D": np.array([0, 1]),
    "L": np.array([-1, 0]),
    "R": np.array([1, 0]),
}


def part1(lines: list[str]):
    pos_head = np.array([0, 0])
    pos_tail = np.array([0, 0])
    hist_tail = {tuple(pos_tail)}
    for line in lines:
        direction, repetition = line.strip().split()
        direction, repetition = directions[direction], int(repetition)
        for _ in range(repetition):
            pos_head += direction
            if np.all(np.abs(pos_head - pos_tail) <= 1):
                continue
            pos_tail += np.sign(pos_head - pos_tail)
            hist_tail.add(tuple(pos_tail))
    return len(hist_tail)


def part2(lines: list[str]):
    rope_length = 10
    rope = [np.array([0, 0]) for _ in range(rope_length)]
    hist_tail = {tuple(rope[-1])}

    for line in lines:
        direction, repetition = line.strip().split()
        direction, repetition = directions[direction], int(repetition)
        for _ in range(repetition):
            rope[0] += direction
            for index in range(1, len(rope)):
                if np.all(np.abs(rope[index - 1] - rope[index]) <= 1):
                    continue
                rope[index] += np.sign(rope[index - 1] - rope[index])
            hist_tail.add(tuple(rope[-1]))
    return len(hist_tail)


def test():
    with open("d09-t1.txt") as f:
        lines = f.readlines()
    assert part1(lines) == 13
    assert part2(lines) == 1
    with open("d09-t2.txt") as f:
        lines = f.readlines()
    assert part2(lines) == 36


if __name__ == "__main__":
    with open("input/09.txt") as f:
        lines = f.readlines()
    print(part1(lines), part2(lines))
