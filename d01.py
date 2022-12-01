def get_elves(content: str):
    elves = content.split("\n\n")
    elves = [
        sum(int(calorie) for calorie in elf.split("\n") if calorie) for elf in elves
    ]
    return elves


def part1(content):
    return max(get_elves(content))


def part2(content):
    elves = get_elves(content)
    elves.sort(reverse=True)
    return sum(elves[:3])


def test():
    with open("d01-t.txt") as f:
        test_content = f.read()
    assert part1(test_content) == 24000
    assert part2(test_content) == 45000


if __name__ == "__main__":
    with open("input/01.txt") as f:
        content = f.read()
    print(part1(content), part2(content))
