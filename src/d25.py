values = {c: v for c, v in zip(["=", "-", "0", "1", "2"], range(-2, 3))}
reverse_values = {v: k for k, v in values.items()}


def snafu_to_int(snafu):
    return sum(
        values[c] * 5 ** (len(snafu) - index - 1) for index, c in enumerate(snafu)
    )


def int_to_snafu(number):
    snafu_digits = []
    while number != 0:
        remainder = number % 5
        if remainder not in reverse_values:
            remainder -= 5
            number += 5
        snafu_digits.append(reverse_values[remainder])
        number //= 5
    return "".join(reversed(snafu_digits))


def part1(lines):
    number = sum(snafu_to_int(line.strip()) for line in lines)
    return int_to_snafu(number)


def test():
    with open("d25-t.txt") as f:
        lines = f.readlines()
    assert part1(lines) == "2=-1=0"


if __name__ == "__main__":
    with open("input/25.txt") as f:
        lines = f.readlines()
    print(part1(lines))
