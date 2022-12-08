def generate_root(lines: list[str]):
    root = {}
    stack = [root]
    for line in lines:
        match line.strip().split():
            case ["$", "ls"]:
                continue
            case ["$", "cd", "/"]:
                stack = [root]
            case ["$", "cd", ".."]:
                stack.pop()
            case ["$", "cd", directory]:
                stack.append(stack[-1][directory])
            case ["dir", directory]:
                stack[-1][directory] = {}
            case [number, file]:
                number = int(number)
                stack[-1][file] = number
    return root


def part1(lines):
    def search(directory):
        total_size = 0
        sum_small_size = 0
        for child in directory.values():
            if isinstance(child, int):
                total_size += child
            else:
                size, small_directory_size = search(child)
                total_size += size
                sum_small_size += small_directory_size
        if total_size <= 100_000:
            sum_small_size += total_size
        return total_size, sum_small_size

    return search(generate_root(lines))[1]


def part2(lines):
    def total_size(directory, action=None):
        acc = 0
        for child in directory.values():
            if isinstance(child, int):
                acc += child
            else:
                acc += total_size(child, action)
        if action is not None:
            action(acc)
        return acc

    root = generate_root(lines)
    occupied_spce = total_size(root)
    need_free = 30_000_000 - (70_000_000 - occupied_spce)

    delete_directory_size = occupied_spce

    def record(size):
        nonlocal delete_directory_size
        if need_free < size < delete_directory_size:
            delete_directory_size = size

    total_size(root, record)
    return delete_directory_size


def test():
    with open("d07-t.txt") as f:
        lines = f.readlines()
    assert part1(lines) == 95437
    assert part2(lines) == 24933642


if __name__ == "__main__":
    with open("input/07.txt") as f:
        lines = f.readlines()
    print(part1(lines), part2(lines))
