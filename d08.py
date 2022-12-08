import itertools


def part1(lines):
    grid = [[int(c) for c in line.strip()] for line in lines]
    visible = [[False] * len(grid[0]) for _ in range(len(grid))]

    for row in range(len(grid)):
        max_height = -1
        for col in range(len(grid[0])):
            if grid[row][col] > max_height:
                visible[row][col] = True
            max_height = max(max_height, grid[row][col])
        max_height = -1
        for col in reversed(range(len(grid[0]))):
            if grid[row][col] > max_height:
                visible[row][col] = True
            max_height = max(max_height, grid[row][col])
    for col in range(len(grid[0])):
        max_height = -1
        for row in range(len(grid)):
            if grid[row][col] > max_height:
                visible[row][col] = True
            max_height = max(max_height, grid[row][col])
        max_height = -1
        for row in reversed(range(len(grid))):
            if grid[row][col] > max_height:
                visible[row][col] = True
            max_height = max(max_height, grid[row][col])
    return sum(sum(line) for line in visible)


def part2(lines):
    grid = [[int(c) for c in line.strip()] for line in lines]
    best_score = 0
    for house_row, house_col in itertools.product(
        range(len(grid)), range(len(grid[0]))
    ):
        up = down = left = right = 0
        house_height = grid[house_row][house_col]
        for row in range(house_row + 1, len(grid)):
            down += 1
            if grid[row][house_col] >= house_height:
                break
        for row in range(house_row - 1, -1, -1):
            up += 1
            if grid[row][house_col] >= house_height:
                break
        for col in range(house_col + 1, len(grid)):
            right += 1
            if grid[house_row][col] >= house_height:
                break
        for col in range(house_col + -1, -1, -1):
            left += 1
            if grid[house_row][col] >= house_height:
                break
        best_score = max(best_score, up * down * left * right)
    return best_score


def test():
    with open("d08-t.txt") as f:
        lines = f.readlines()
    assert part1(lines) == 21
    assert part2(lines) == 8


if __name__ == "__main__":
    with open("input/08.txt") as f:
        lines = f.readlines()
    print(part1(lines), part2(lines))
