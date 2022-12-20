def mix(nums: list[int], original_indexes=None, current_indexes=None):
    if not original_indexes:
        original_indexes = list(range(len(nums)))
        current_indexes = list(range(len(nums)))

    for original_index in range(len(nums)):
        index = current_indexes[original_index]
        num = nums[index]
        direction = 1
        for _ in range(num % (len(nums) - 1)):
            swap_index = (index + direction) % len(nums)
            swap_original_index = original_indexes[swap_index]
            nums[index], nums[swap_index] = (
                nums[swap_index],
                nums[index],
            )
            current_indexes[original_index], current_indexes[swap_original_index] = (
                current_indexes[swap_original_index],
                current_indexes[original_index],
            )
            original_indexes[index], original_indexes[swap_index] = (
                original_indexes[swap_index],
                original_indexes[index],
            )
            index = swap_index


def part1(lines: list[str]):
    encrypted = [int(line.strip()) for line in lines]
    mix(encrypted)
    zero_index = encrypted.index(0)
    selected_indices = (
        (zero_index + shift) % len(encrypted) for shift in [1000, 2000, 3000]
    )
    return sum(encrypted[index] for index in selected_indices)


def part2(lines: list[str]):
    encrypted = [int(line.strip()) * 811589153 for line in lines]
    original_indexes = list(range(len(encrypted)))
    current_indexes = list(range(len(encrypted)))
    for _ in range(10):
        mix(encrypted, original_indexes, current_indexes)
    zero_index = encrypted.index(0)
    selected_indices = (
        (zero_index + shift) % len(encrypted) for shift in [1000, 2000, 3000]
    )
    return sum(encrypted[index] for index in selected_indices)


def test():
    with open("d20-t.txt") as f:
        lines = f.readlines()
    assert part1(lines) == 3
    assert part2(lines) == 1623178306


if __name__ == "__main__":
    with open("input/20.txt") as f:
        lines = f.readlines()
    print(part1(lines))
    print(part2(lines))
