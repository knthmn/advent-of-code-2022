directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def parse_input(lines: list[str]):
    def parse_path(line: str):
        number_buffer = []
        for c in line.strip():
            if c.isdigit():
                number_buffer.append(c)
            else:
                if number_buffer:
                    yield int("".join(number_buffer))
                    number_buffer.clear()
                yield c
        yield int("".join(number_buffer))

    board = [line.rstrip() for line in lines[:-2]]
    len_x, len_y = max(len(line) for line in board), len(board)
    x, y = board[0].index("."), 0
    board = {
        (x, y): c
        for y, line in enumerate(board)
        for x, c in enumerate(line)
        if c != " "
    }

    return board, parse_path(lines[-1]), (x, y), (len_x, len_y)


def part1(lines: list[str]):
    board, path, (x, y), (len_x, len_y) = parse_input(lines)

    def move(ix, iy, dx, dy):
        x, y = ix, iy
        while True:
            x, y = (x + dx) % len_x, (y + dy) % len_y
            if (x, y) not in board:
                continue
            if board[(x, y)] == ".":
                return x, y
            if board[(x, y)] == "#":
                return None

    direction_index = 0
    for instruction in path:
        if isinstance(instruction, str):
            direction_index = (
                direction_index + (1 if instruction == "R" else -1)
            ) % len(directions)
        else:
            dx, dy = directions[direction_index]
            for _ in range(instruction):
                pos = move(x, y, dx, dy)
                if not pos:
                    break
                x, y = pos

    return 1000 * (y + 1) + 4 * (x + 1) + direction_index
    pass


def part2(lines, helper_lines, region_size):
    board, path, (x, y), _ = parse_input(lines)

    def sign(a):
        return 1 if a > 0 else 0 if a == 0 else -1

    portals = {}
    for line in helper_lines:
        bx1, by1, ex1, ey1, bx2, by2, ex2, ey2 = [
            int(num) for num in line.strip().split(",")
        ]
        portals[(bx1, by1, ex1, ey1)] = bx2, by2, sign(bx2 - ex2), sign(by2 - ey2)
        portals[(bx2, by2, ex2, ey2)] = bx1, by1, sign(bx1 - ex1), sign(by1 - ey1)

    def move(x, y, dx, dy):
        nx, ny = (x + dx), (y + dy)
        if (nx, ny) not in board:
            nrx, nry, ndx, ndy = portals[
                tuple(a // region_size for a in (x, y, nx, ny))
            ]
            if dx == 1:
                exit_location = y % region_size
            elif dx == -1:
                exit_location = region_size - 1 - (y % region_size)
            elif dy == -1:
                exit_location = x % region_size
            elif dy == 1:
                exit_location = (region_size - 1) - (x % region_size)
            if ndx != 0:
                nmx = 0 if ndx == 1 else region_size - 1
                nmy = exit_location if ndx == 1 else region_size - 1 - exit_location
            else:
                nmy = 0 if ndy == 1 else region_size - 1
                nmx = exit_location if ndy == -1 else region_size - 1 - exit_location
            nx = nrx * region_size + nmx
            ny = nry * region_size + nmy
            dx, dy = ndx, ndy
        x, y = nx, ny

        if board[(x, y)] == ".":
            return x, y, dx, dy
        if board[(x, y)] == "#":
            return None

    direction_index = 0
    for instruction in path:
        if isinstance(instruction, str):
            direction_index = (
                direction_index + (1 if instruction == "R" else -1)
            ) % len(directions)
        else:
            dx, dy = directions[direction_index]
            for _ in range(instruction):
                new_state = move(x, y, dx, dy)
                if not new_state:
                    break
                x, y, dx, dy = new_state
            direction_index = directions.index((dx, dy))

    return 1000 * (y + 1) + 4 * (x + 1) + direction_index

"""
The helper file is computed by hand, consists of 6 pairs or corresponding edges.
An edge is given by the coords of the map region, and the coords of the off map region.
Example is given in d22-th.txt
"""

def test():
    with open("d22-t.txt") as f:
        lines = f.readlines()
    with open("d22-th.txt") as f:
        helper_lines = f.readlines()
    assert part1(lines) == 6032
    assert part2(lines, helper_lines, 4) == 5031


if __name__ == "__main__":
    with open("input/22.txt") as f:
        lines = f.readlines()
    with open("input/22h.txt") as f:
        helper_lines = f.readlines()
    print(part1(lines))
    print(part2(lines, helper_lines, 50))
