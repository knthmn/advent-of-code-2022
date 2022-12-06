def find_marker_index(signal: str, length: int):
    for index in range(len(signal) - length):
        if len(set(signal[index : index + length])) == length:
            return index + length


def test():
    assert find_marker_index("bvwbjplbgvbhsrlpgdmjqwftvncz", 4) == 5
    assert find_marker_index("nppdvjthqldpwncqszvftbrmjlhg", 4) == 6
    assert find_marker_index("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4) == 10
    assert find_marker_index("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4) == 11


if __name__ == "__main__":
    with open("input/06.txt") as f:
        signal = f.read()
    print(find_marker_index(signal, 4))
    print(find_marker_index(signal, 14))
