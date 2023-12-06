import argparse
import time
from math import ceil, floor


def read_file(fname):
    times = []
    distances = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip.startswith("Time"):
                times = [int(i) for i in strip.split()[1:]]
            elif strip.startswith("Distance"):
                distances = [int(i) for i in strip.split()[1:]]

    return times, distances


def compute_start_end(time, d_to_beat):
    # quadratic formula
    x1 = (-time + (time**2 - 4 * d_to_beat) ** 0.5) / -2
    x2 = (-time - (time**2 - 4 * d_to_beat) ** 0.5) / -2
    min_x = ceil(min(x1, x2))
    max_x = floor(max(x1, x2))
    while min_x * (time - min_x) <= d_to_beat:
        # catch when you match the distance instad of beat
        min_x += 1
    while max_x * (time - max_x) <= d_to_beat:
        # catch when you match the distance instad of beat
        max_x -= 1
    return min_x, max_x


def part_1(data):
    out = 1
    for t, d in zip(*data):
        options = compute_start_end(t, d)
        out *= options[1] - options[0] + 1

    return out


def part_2(data):
    t = int("".join(str(i) for i in data[0]))
    d = int("".join(str(i) for i in data[1]))
    options = compute_start_end(t, d)
    return options[1] - options[0] + 1


def main(fname):
    start = time.time()
    data = read_file(fname)
    total_1 = part_1(data)
    t1 = time.time()
    print(f"Part 1: {total_1}")
    print(f"Ran in {t1-start} s")
    total_2 = part_2(data)
    print(f"Part 2: {total_2}")
    print(f"Ran in {time.time()-t1} s")
    print(f"Total ran in {time.time()-start} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename
    main(filename)
