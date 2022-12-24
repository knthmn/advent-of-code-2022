def find_quickest(lines: list[str], acquire_snack=False):
    walls = set()
    blizzards = []
    len_x, len_y = len(lines[0].strip()), len(lines)
    init_pos, final_pos = (1, 0), (len_x - 2, len_y - 1)
    target_pos = final_pos
    remaining_legs = 3 if acquire_snack else 1
    for y, line in enumerate(lines):
        for x, c in enumerate(line.strip()):
            if c == "#":
                walls.add((x, y))
            elif c == "<":
                blizzards.append((x, y, -1, 0))
            elif c == ">":
                blizzards.append((x, y, 1, 0))
            elif c == "^":
                blizzards.append((x, y, 0, -1))
            elif c == "v":
                blizzards.append((x, y, -0, 1))
    t = 0
    possible_positions = {init_pos}
    while True:
        new_blizzards = []
        for (x, y, dx, dy) in blizzards:
            while True:
                x, y = (x + dx) % len_x, (y + dy) % len_y
                if (x, y) not in walls:
                    break
            new_blizzards.append((x, y, dx, dy))
        blizzards = new_blizzards
        blizzard_positions = {(x, y) for x, y, _, _, in blizzards}
        new_possible_positions = set()
        for x, y in possible_positions:
            for nx, ny in [(x, y), (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                if (
                    0 <= nx < len_x
                    and 0 <= ny < len_y
                    and (nx, ny) not in blizzard_positions
                    and (nx, ny) not in walls
                ):
                    new_possible_positions.add((nx, ny))
        possible_positions = new_possible_positions
        t += 1

        if target_pos in possible_positions:
            remaining_legs -= 1
            if remaining_legs == 0:
                return t
            possible_positions = {target_pos}
            target_pos = (init_pos, final_pos)[remaining_legs % 2]


def test():
    with open("d24-t.txt") as f:
        lines = f.readlines()
    assert find_quickest(lines) == 18
    assert find_quickest(lines, acquire_snack=True) == 54


if __name__ == "__main__":
    with open("input/24.txt") as f:
        lines = f.readlines()
    print(find_quickest(lines))
    print(find_quickest(lines, acquire_snack=True))
