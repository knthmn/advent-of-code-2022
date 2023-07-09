from collections import deque
from dataclasses import dataclass
import math
from typing import Generator, Literal, Self


@dataclass(slots=True, frozen=True)
class Vec2:
    x: int
    y: int

    def rotate(self, amount: int) -> Self:
        """Rotates the vector by 90 degrees clockwise for {amount} times."""
        amount = amount % 4
        if amount == 0:
            return self
        elif amount == 1:
            return Vec2(-self.y, self.x)
        elif amount == 2:
            return Vec2(-self.x, -self.y)
        else:
            return Vec2(self.y, -self.x)

    def __add__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vec2") -> "Vec2":
        return Vec2(self.x - other.x, self.y - other.y)


cardinal_directions = [Vec2(1, 0).rotate(n) for n in range(4)]


def parse_input(
    lines: list[str],
) -> tuple[dict[Vec2, str], Generator[int | Literal["L", "R"], None, None], Vec2, Vec2]:
    def parse_path(line: str):
        number_buffer: list[str] = []
        for c in line.strip():
            if c.isdigit():
                number_buffer.append(c)
            elif c == "L" or c == "R":
                if number_buffer:
                    yield int("".join(number_buffer))
                    number_buffer.clear()
                yield c
            else:
                raise ValueError(f"Invalid character in path: {c}")
        yield int("".join(number_buffer))

    board = [line.rstrip() for line in lines[:-2]]
    len_x, len_y = max(len(line) for line in board), len(board)
    start_x, start_y = board[0].index("."), 0
    board = {
        Vec2(x, y): c
        for y, line in enumerate(board)
        for x, c in enumerate(line)
        if c != " "
    }
    return board, parse_path(lines[-1]), Vec2(start_x, start_y), Vec2(len_x, len_y)


def part1(lines: list[str]):
    board, path, position, size = parse_input(lines)

    def move(position: Vec2, direction: Vec2) -> tuple[Vec2, bool]:
        target_position = position
        while True:
            target_position = target_position + direction
            target_position = Vec2(
                target_position.x % size.x, target_position.y % size.y
            )
            if target_position not in board:
                continue
            if board[target_position] == ".":
                return target_position, True
            if board[target_position] == "#":
                return position, False

    direction = Vec2(1, 0)
    for instruction in path:
        if instruction == "L":
            direction = direction.rotate(-1)
        elif instruction == "R":
            direction = direction.rotate(1)
        else:
            for _ in range(instruction):
                position, moved = move(position, direction)
                if not moved:
                    break
    return (
        1000 * (position.y + 1)
        + 4 * (position.x + 1)
        + cardinal_directions.index(direction)
    )


def part2(lines: list[str]) -> int:
    board, path, position, size = parse_input(lines)

    grid_size = int(math.sqrt(len(board) // 6))
    grids = {
        Vec2(sx, sy)
        for sx in range(size.x // grid_size)
        for sy in range(size.y // grid_size)
        if Vec2(sx * grid_size, sy * grid_size) in board
    }

    # find all the edges arranged clockwise
    first_grid = min(grids, key=lambda square: (square.y, square.x))
    edges = [(first_grid, Vec2(0, -1))]
    while len(edges) != 14:
        grid, edge_direction = edges[-1]
        if grid + edge_direction.rotate(1) not in grids:
            edges.append((grid, edge_direction.rotate(1)))
        elif grid + edge_direction + edge_direction.rotate(1) not in grids:
            edges.append((grid + edge_direction.rotate(1), edge_direction))
        else:
            edges.append(
                (
                    grid + edge_direction + edge_direction.rotate(1),
                    edge_direction.rotate(-1),
                )
            )

    # find find all the edges that are separated by inner bend to each other
    search_edges_indexes: deque[tuple[int, int, int]] = deque()
    matched_edges_indexes: dict[int, int] = {}
    for i in range(len(edges)):
        edge1, edge2 = edges[i], edges[(i + 1) % len(edges)]
        if edge1[0] + edge1[1] == edge2[0] + edge2[1]:
            search_edges_indexes.append((i, (i + 1) % len(edges), 1))

    # expand out to matching edges that are further apart
    while search_edges_indexes:
        index1, index2, level = search_edges_indexes.popleft()
        edge1, edge2 = edges[index1], edges[index2]
        # whether the edges are in the same direction (vertical / horizontal)
        # depends on if the level (starting from 1 for inner bend edges)
        # is even or odd. Without checking this the expansion can be wrong.
        if (level % 2 == 0) != ((edge1[1].x == 0) == (edge2[1].x == 0)):
            continue
        if index1 in matched_edges_indexes:
            continue
        matched_edges_indexes[index1] = index2
        matched_edges_indexes[index2] = index1
        search_edges_indexes.append(
            ((index1 - 1) % len(edges), (index2 + 1) % len(edges), level + 1)
        )
    matched_edges = {
        edges[index1]: edges[index2] for index1, index2 in matched_edges_indexes.items()
    }

    def move(position: Vec2, direction: Vec2) -> tuple[Vec2, Vec2, bool]:
        target_position = position + direction
        target_direction = direction
        if target_position not in board:
            grid = Vec2(position.x // grid_size, position.y // grid_size)
            shift = Vec2(position.x % grid_size, position.y % grid_size)
            receiving_grid, receiving_direction = matched_edges[(grid, direction)]
            receiving_direction = receiving_direction.rotate(2)
            num_rotations = (
                -cardinal_directions.index(direction)
                + cardinal_directions.index(receiving_direction)
            ) % 4
            for _ in range(num_rotations):
                shift = Vec2(grid_size - 1 - shift.y, shift.x)
            new_position = Vec2(
                (receiving_grid.x - receiving_direction.x) * grid_size + shift.x,
                (receiving_grid.y - receiving_direction.y) * grid_size + shift.y,
            )
            target_position = new_position + receiving_direction
            target_direction = receiving_direction
        if board[target_position] == "#":
            return position, direction, False
        return target_position, target_direction, True

    direction = Vec2(1, 0)
    for instruction in path:
        if instruction == "L":
            direction = direction.rotate(-1)
        elif instruction == "R":
            direction = direction.rotate(1)
        else:
            for _ in range(instruction):
                position, direction, moved = move(position, direction)
                if not moved:
                    break
    return (
        1000 * (position.y + 1)
        + 4 * (position.x + 1)
        + cardinal_directions.index(direction)
    )


def test():
    with open("d22-t.txt") as f:
        lines = f.readlines()
    assert part1(lines) == 6032
    assert part2(lines) == 5031


if __name__ == "__main__":
    with open("input/22.txt") as f:
        lines = f.readlines()
    print(part1(lines))
    print(part2(lines))
