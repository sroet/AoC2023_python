import argparse
import time
from functools import cache


def read_file(fname):
    status = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                records, numbers = strip.split()
                numbers = tuple(int(i) for i in numbers.split(","))
                status.append((records, numbers))

    return status


# Caching is important, took runtime of the example down from 1.5 s to 1.8 ms!
@cache
def gen_options(numbers, reference, start=1):
    length = len(reference)
    if len(numbers) != 0:
        my_number = numbers[0]
        left_numbers = numbers[1:]
    else:
        if any(i == "#" for i in reference):
            # We will only be adding '.' so this will never work
            return 0
        return 1

    max_input = length - (sum(numbers) + len(numbers) - 1)
    if max_input <= 0:
        return 1

    out = 0
    for i in range(start, max_input + 1):
        diff = i + my_number
        if any(c == "#" for c in reference[:i]):
            # We are adding '.' so this will only become worse for later i
            break
        if any(c == "." for c in reference[i:diff]):
            # might be solvable
            continue
        out += gen_options(left_numbers, reference[diff:])
    return out


def part_1(data):
    out = 0
    for line, numbers in data:
        out += gen_options(numbers, line, 0)
    return out


def part_2(data):
    out = 0
    i = 0
    for line, numbers in data:
        line = "?".join([line] * 5)
        numbers *= 5
        out += gen_options(numbers, line, 0)
        i += 1
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
