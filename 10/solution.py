import argparse
import time
from collections import deque
from math import floor, ceil


def read_file(fname):
    data = []
    start = (0, 0)
    with open(fname, "r") as file:
        for y, line in enumerate(file):
            strip = line.strip()
            if strip != "":
                data.append([c for c in strip])
                if "S" in strip:
                    start = (strip.index("S"), y)
    return data, start


next_map = {
    "|": "NS",
    "-": "EW",
    "L": "NE",
    "J": "NW",
    "7": "SW",
    "F": "SE",
}

oposite_map = {"E": "W", "W": "E", "N": "S", "S": "N"}


def next_point(current_point, direction):
    x, y = current_point
    match direction:
        case "N":
            return (x, y - 1)
        case "S":
            return (x, y + 1)
        case "E":
            return (x + 1, y)
        case "W":
            return (x - 1, y)


def part_1(data):
    done = {}
    data, start = data
    current_step = 0
    # Find type of start
    x, y = start
    todo = deque()
    # find start directions
    done[start] = current_step
    for direction in "NSEW":
        x_next, y_next = next_point(start, direction)
        next_type = data[y_next][x_next]
        if next_type in next_map and oposite_map[direction] in next_map[next_type]:
            next_direction = [
                c for c in next_map[next_type] if c != oposite_map[direction]
            ][0]
            todo.append(((x_next, y_next), next_direction, current_step + 1))
    done[start] = 0
    while todo:
        current_point, next_direction, current_step = todo.popleft()
        if current_point in done:
            return done[current_point], done
        done[current_point] = current_step
        next_x, next_y = next_point(current_point, next_direction)
        next_type = data[next_y][next_x]
        next_direction = [
            c for c in next_map[next_type] if c != oposite_map[next_direction]
        ][0]
        todo.append(((next_x, next_y), next_direction, current_step + 1))


def connected(point1, point2, loop):
    if point1 not in loop or point2 not in loop:
        return False
    if abs(loop[point1] - loop[point2]) != 1:
        return False
    return True


def generate_outside_points(current_point, loop):
    x, y = current_point
    up_y = floor(y)
    down_y = ceil(y)
    left_x = floor(x)
    right_x = ceil(x)
    # test up
    if not connected((left_x, up_y), (right_x, up_y), loop):
        yield x, y - 1
    # test down
    if not connected((left_x, down_y), (right_x, down_y), loop):
        yield x, y + 1
    # test left
    if not connected((left_x, down_y), (left_x, up_y), loop):
        yield x - 1, y
    # test right
    if not connected((right_x, down_y), (right_x, up_y), loop):
        yield x + 1, y


def part_2(data, loop):
    data, _ = data
    min_x, max_x = len(data[0]) + 1, 0
    min_y, max_y = len(data) + 1, 0
    for x, y in loop.keys():
        min_x = min(x, min_x)
        max_x = max(x, max_x)
        min_y = min(y, min_y)
        max_y = max(y, max_y)
    # use halfpoints
    start = min_x - 0.5, min_y - 0.5
    outside = set([start])
    todo = deque()
    current_point = start
    todo.append(current_point)
    while todo:
        for x, y in generate_outside_points(current_point, loop):
            if (x, y) in outside:
                continue
            if min_x - 0.5 <= x <= max_x + 0.5 and min_y - 0.5 <= y <= max_y + 0.5:
                outside.add((x, y))
                todo.append((x, y))
        current_point = todo.popleft()
    out = 0
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if (x, y) in loop:
                continue
            edges = [
                (x - 0.5, y - 0.5),
                (x + 0.5, y - 0.5),
                (x - 0.5, y + 0.5),
                (x + 0.5, y + 0.5),
            ]
            if not any(e in outside for e in edges):
                out += 1
    return out


def main(fname):
    start = time.time()
    data = read_file(fname)
    total_1, loop = part_1(data)
    t1 = time.time()
    print(f"Part 1: {total_1}")
    print(f"Ran in {t1-start} s")
    total_2 = part_2(data, loop)
    print(f"Part 2: {total_2}")
    print(f"Ran in {time.time()-t1} s")
    print(f"Total ran in {time.time()-start} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename
    main(filename)
