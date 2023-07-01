import functools
import operator
import re
import typing
from fractions import Fraction


class Equation(typing.NamedTuple):
    left_name: str
    right_name: str
    op: str


def get_monkeys(lines: list[str]):
    monkeys = {}
    for line in lines:
        if match := re.match(
            r"""([a-z]{4}): ([a-z]{4}) ([\+\-\*/]) ([a-z]{4})""", line.strip()
        ):
            monkey_name, name1, op, name2 = match.groups()
            monkeys[monkey_name] = Equation(name1, name2, op)
        else:
            monkey_name, number = line.split(":")
            monkeys[monkey_name] = int(number.strip())
    return monkeys


def get_memorized_evaluate(monkeys):
    ops = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.floordiv,
    }

    @functools.cache
    def evaluate(monkey_name):
        monkey = monkeys[monkey_name]
        if not isinstance(monkey, Equation):
            return monkey
        left_name, right_name, op = monkey
        left, right = evaluate(left_name), evaluate(right_name)
        return ops[op](left, right)

    return evaluate


def part1(lines: list[str]):
    monkeys = get_monkeys(lines)
    return get_memorized_evaluate(monkeys)("root")


class Amount(typing.NamedTuple):
    linear: Fraction
    const: Fraction

    def __add__(self, other):
        if isinstance(other, int):
            return Amount(self.linear, self.const + other)
        return Amount(self.linear + other.linear, self.const + other.const)

    def __radd__(self, other):
        return self + other

    def __neg__(self):
        return Amount(-self.linear, -self.const)

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        if isinstance(other, int):
            return Amount(self.linear * other, self.const * other)
        raise ValueError("Monkey bad at math")

    def __rmul__(self, other):
        return self * other

    def __floordiv__(self, other):
        if isinstance(other, int):
            return Amount(self.linear / other, self.const / other)
        raise ValueError("Monkey bad at math")

    def __rfloordiv__(self, other):
        raise ValueError("Monkey bad at math")


def part2(lines: list[str]):
    monkeys = get_monkeys(lines)
    monkeys["humn"] = Amount(Fraction(1, 1), Fraction(0, 1))
    evaluate = get_memorized_evaluate(monkeys)
    left, right, _ = monkeys["root"]
    left, right = evaluate(left), evaluate(right)
    if isinstance(left, int):
        left = Amount(Fraction(0, 1), Fraction(left, 1))
    if isinstance(right, int):
        right = Amount(Fraction(0, 1), Fraction(right, 1))
    answer = (right.const - left.const) / (left.linear - right.linear)
    return int(answer)


def test():
    with open("d21-t.txt") as f:
        lines = f.readlines()
    assert part1(lines) == 152
    assert part2(lines) == 301


if __name__ == "__main__":
    with open("input/21.txt") as f:
        lines = f.readlines()
    print(part1(lines))
    print(part2(lines))
