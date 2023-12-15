import argparse
import time
from collections import defaultdict


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                data.append(strip.split(","))
    return data[0]


def hash_func(string):
    out = 0
    for c in string:
        out += ord(c)
        out *= 17
        out %= 256
    return out


def part_1(data):
    out = 0
    for string in data:
        out += hash_func(string)
    return out


def part_2(data):
    # use dictionaries as they are ordered hashmaps in modern python 3
    boxes = defaultdict(dict)
    for line in data:
        if "-" in line:
            label = line.strip("-")
            # silent pop the lens if present
            boxes[hash_func(label)].pop(label, None)
        elif "=" in line:
            label, f_length = line.split("=")
            boxes[hash_func(label)][label] = int(f_length)
    out = 0
    for box, lenses in boxes.items():
        # don't care about the lens label anymore
        for lens_number, f_length in enumerate(lenses.values(), 1):
            temp = 1
            temp *= box + 1
            temp *= lens_number
            temp *= f_length
            out += temp
    return out


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
