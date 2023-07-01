import dataclasses
import math
import re
from typing import Literal, Callable

Operand = Literal["old"] | int


@dataclasses.dataclass
class Monkey:
    items: list[int]
    operator: Literal["+", "*"]
    operand1: Operand
    operand2: Operand
    divisibility: int
    true_index: int
    false_index: int
    num_processed: int = 0

    @staticmethod
    def _parse(lines: list[str]):
        items = [int(number.strip()) for number in lines[1][18:].split(",")]
        operand1, operator, operand2 = re.match(
            R"""\s+Operation: new = (old|\d+) ([+*]) (old|\d+)""", lines[2]
        ).groups()
        operand1 = int(operand1) if operand1.isnumeric() else operand1
        operand2 = int(operand2) if operand2.isnumeric() else operand2
        divisibility = int(lines[3][21:].strip())
        true_index = int(lines[4][29:].strip())
        false_index = int(lines[5][30:].strip())
        return Monkey(
            items, operator, operand1, operand2, divisibility, true_index, false_index
        )

    @staticmethod
    def parse_monkeys(lines: list[str]) -> list["Monkey"]:
        return [
            Monkey._parse(lines[index * 7 : (index + 1) * 7])
            for index in range((len(lines) + 1) // 7)
        ]

    def inspect(self, monkeys: list["Monkey"], tame: Callable[[int], int]):
        for item in self.items:
            operand1 = item if self.operand1 == "old" else self.operand1
            operand2 = item if self.operand2 == "old" else self.operand2
            new_item = (
                operand1 + operand2 if self.operator == "+" else operand1 * operand2
            )
            new_item = tame(new_item)
            target_monkey = monkeys[
                self.true_index
                if new_item % self.divisibility == 0
                else self.false_index
            ]
            self.num_processed += 1
            target_monkey.items.append(new_item)
        self.items.clear()


def part1(lines: list[str]):
    monkeys = Monkey.parse_monkeys(lines)
    for _ in range(20):
        for monkey in monkeys:
            monkey.inspect(monkeys, lambda item: item // 3)
    nums_processed = [monkey.num_processed for monkey in monkeys]
    nums_processed.sort()
    return nums_processed[-1] * nums_processed[-2]


def part2(lines: list[str]):
    monkeys = Monkey.parse_monkeys(lines)
    factor = math.lcm(*[monkey.divisibility for monkey in monkeys])
    for _ in range(10000):
        for monkey in monkeys:
            monkey.inspect(monkeys, lambda item: item % factor)
    nums_processed = [monkey.num_processed for monkey in monkeys]
    nums_processed.sort()
    return nums_processed[-1] * nums_processed[-2]


def test():
    with open("d11-t.txt") as f:
        lines = f.readlines()
    assert part1(lines) == 10605
    assert part2(lines) == 2713310158


if __name__ == "__main__":
    with open("input/11.txt") as f:
        lines = f.readlines()
    print(part1(lines))
    print(part2(lines))
