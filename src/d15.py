import re


def parse_entries(lines: list[str]):
    pattern = re.compile(
        R"""Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at x=([-\d]+), y=([-\d]+)"""
    )
    return [
        tuple(int(coord) for coord in pattern.match(line).groups()) for line in lines
    ]


def part1(lines: list[str], target_y):
    entries = parse_entries(lines)
    ruled_out_regions = []
    for sensor_x, sensor_y, beacon_x, beacon_y in entries:
        distance = abs(beacon_y - sensor_y) + abs(beacon_x - sensor_x)
        distance_from_target = abs(sensor_y - target_y)
        if distance < distance_from_target:
            continue
        width = distance - distance_from_target
        current_start, current_end = sensor_x - width, sensor_x + width
        new_ruled_out_regions = []
        for start, end in ruled_out_regions:
            if max(start, current_start) <= min(end, current_end) + 1:
                current_start = min(start, current_start)
                current_end = max(end, current_end)
            else:
                new_ruled_out_regions.append((start, end))
        new_ruled_out_regions.append((current_start, current_end))
        ruled_out_regions = new_ruled_out_regions
        ruled_out_regions.sort(key=lambda region: region[0])
    beacons_in_region = set(
        beacon_x
        for _, _, beacon_x, beacon_y in entries
        if beacon_y == target_y
        and any(start <= beacon_x <= end for start, end in ruled_out_regions)
    )
    region_size = sum(region[1] - region[0] + 1 for region in ruled_out_regions)
    return region_size - len(beacons_in_region)


def part2(lines: list[str], search_space):
    entries = parse_entries(lines)
    entries = [
        (sensor_x, sensor_y, abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y))
        for sensor_x, sensor_y, beacon_x, beacon_y in entries
    ]

    def boundary(sensor_x, sensor_y, distance):
        distance += 1
        for displacement in range(-distance, distance + 1):
            displacement_y = distance - abs(displacement)
            yield sensor_x + displacement, sensor_y + displacement_y
            if displacement_y != 0:
                yield sensor_x + displacement, sensor_y - displacement_y

    possible_locations = (
        (x, y)
        for sensor_x, sensor_y, distance in entries
        for (x, y) in boundary(sensor_x, sensor_y, distance)
    )
    valid_locations = (
        (x, y)
        for (x, y) in possible_locations
        if 0 <= x <= search_space
        and 0 <= y <= search_space
        and all(
            abs(x - sensor_x) + abs(y - sensor_y) > distance
            for sensor_x, sensor_y, distance in entries
        )
    )
    distress_x, distress_y = next(valid_locations)
    return distress_x * 4_000_000 + distress_y


def test():
    with open("d15-t.txt") as f:
        lines = f.readlines()
    assert part1(lines, 10) == 26
    assert part2(lines, 20) == 56_000_011


if __name__ == "__main__":
    with open("input/15.txt") as f:
        lines = f.readlines()
    print(part1(lines, 2_000_000))
    print(part2(lines, 4_000_000))
