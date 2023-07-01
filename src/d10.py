def machine(lines):
    x = 1
    cycle = 1
    for line in lines:
        match line.strip().split():
            case ["noop"]:
                yield cycle, x
                cycle += 1
            case ["addx", addend]:
                for _ in range(2):
                    yield cycle, x
                    cycle += 1
                addend = int(addend)
                x += addend
    yield cycle, x


def part1(lines):
    acc = 0
    for cycle, x in machine(lines):
        if (cycle - 20) % 40 == 0:
            acc += cycle * x
    return acc


def part2(lines):
    screen = []
    for cycle, x in machine(lines):
        crt_target = (cycle - 1) % 40
        if x - 1 <= crt_target <= x + 1:
            screen.append("#")
        else:
            screen.append(".")
    screen = [
        screen[row_index * 40 : (row_index + 1) * 40]
        for row_index in range(len(screen) // 40)
    ]
    return "\n".join(("".join(line) for line in screen))


def test():
    with open("d10-t.txt") as f:
        lines = f.readlines()
    assert part1(lines) == 13140
    assert part2(lines) == (
        "##..##..##..##..##..##..##..##..##..##..\n"
        "###...###...###...###...###...###...###.\n"
        "####....####....####....####....####....\n"
        "#####.....#####.....#####.....#####.....\n"
        "######......######......######......####\n"
        "#######.......#######.......#######....."
    )


if __name__ == "__main__":
    with open("input/10.txt") as f:
        lines = f.readlines()
    print(part1(lines))
    print(part2(lines))
